import streamlit as st
import pandas as pd
from banco import conn, cursor
from datetime import datetime

st.title("📊 Dashboard de Comissão")

if not st.session_state.get("logado"):

    st.warning(
        "Faça login primeiro."
    )

    st.stop()

st.success(
    f"👤 Usuário: {st.session_state['nome']}"
)

st.info(
    f"🚚 Função: {st.session_state['funcao']}"
)

funcao = st.session_state["funcao"]

# ==========================
# RESUMO MENSAL
# ==========================

mes_atual = datetime.now().strftime("%m")

cursor.execute(
    """
    SELECT
        cubos,
        clientes,
        comissao
    FROM lancamentos
    WHERE usuario_id = ?
    """,
    (
        st.session_state["id_usuario"],
    )
)

dados = cursor.fetchall()

cubagem_total = 0
clientes_total = 0
comissao_total = 0

for linha in dados:

    cubagem_total += linha[0]
    clientes_total += linha[1]
    comissao_total += linha[2]

st.divider()

st.subheader("📊 Resumo Atual")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📦 Cubagem",
        f"{cubagem_total:.2f}"
    )

with col2:

    st.metric(
        "👥 Clientes",
        int(clientes_total)
    )

with col3:

    st.metric(
        "💰 Comissão",
        f"R$ {comissao_total:.2f}"
    )

# ==========================
# META
# ==========================

meta = 150

progresso = min(
    comissao_total / meta,
    1.0
)

st.subheader("🎯 Meta do Mês")

st.progress(progresso)

st.write(
    f"R$ {comissao_total:.2f} de R$ {meta:.2f}"
)

# ==========================
# ESTATÍSTICAS
# ==========================

if dados:

    maior_cubagem = max(
        linha[0]
        for linha in dados
    )

    maior_comissao = max(
        linha[2]
        for linha in dados
    )

    quantidade = len(dados)

    st.divider()

    st.subheader("📈 Estatísticas")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "📦 Maior Cubagem",
            f"{maior_cubagem:.2f}"
        )

    with c2:

        st.metric(
            "💰 Maior Comissão",
            f"R$ {maior_comissao:.2f}"
        )

    with c3:

        st.metric(
            "📅 Lançamentos",
            quantidade
        )

# ==========================
# NOVO LANÇAMENTO
# ==========================

st.divider()

st.subheader("➕ Novo Lançamento")

cubos = st.number_input(
    "📦 Cubagem",
    min_value=0.0,
    step=0.01,
    format="%.2f"
)

clientes = st.number_input(
    "👥 Clientes Entregues",
    min_value=0,
    step=1
)

if st.button("💰 Calcular Comissão"):

    if cubos <= 0:

        st.error(
            "Informe a cubagem."
        )

        st.stop()

    if funcao == "Auxiliar":

        valor_cubos = cubos * 0.019
        valor_clientes = clientes * 0.21

    else:

        valor_cubos = cubos * 0.038
        valor_clientes = clientes * 0.43

    valor_cubos = round(
        valor_cubos,
        2
    )

    valor_clientes = round(
        valor_clientes,
        2
    )

    comissao = round(
        valor_cubos + valor_clientes,
        2
    )

    st.success(
        f"🏆 Comissão estimada: R$ {comissao:.2f}"
    )

    st.write(
        f"📦 Cubagem: {cubos:.2f}"
    )

    st.write(
        f"👥 Clientes: {clientes}"
    )

    st.write(
        f"💰 Valor Cubagem: R$ {valor_cubos:.2f}"
    )

    st.write(
        f"💰 Valor Clientes: R$ {valor_clientes:.2f}"
    )

    st.write(
        f"🏆 Comissão Total: R$ {comissao:.2f}"
    )

    data_atual = datetime.now().strftime(
        "%d/%m/%Y"
    )

    cursor.execute(
        """
        INSERT INTO lancamentos
        (
            usuario_id,
            data,
            cubos,
            clientes,
            comissao
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            st.session_state["id_usuario"],
            data_atual,
            round(cubos, 2),
            clientes,
            comissao
        )
    )

    conn.commit()

    st.success(
        f"✅ Registro salvo em {data_atual}"
    )

# ==========================
# ÚLTIMOS LANÇAMENTOS
# ==========================

cursor.execute(
    """
    SELECT
        data,
        cubos,
        clientes,
        comissao
    FROM lancamentos
    WHERE usuario_id=?
    ORDER BY id DESC
    LIMIT 5
    """,
    (
        st.session_state["id_usuario"],
    )
)

ultimos = cursor.fetchall()

if ultimos:

    st.divider()

    st.subheader("🕒 Últimos Lançamentos")

    df = pd.DataFrame(
        ultimos,
        columns=[
            "Data",
            "Cubagem",
            "Clientes",
            "Comissão"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

st.divider()

st.warning(
    '''
⚠️ IMPORTANTE

Os valores apresentados são estimativas.

Pode haver pequenas diferenças de centavos
devido aos arredondamentos utilizados pela empresa.

Os registros ficam vinculados apenas ao usuário logado.
'''
)

