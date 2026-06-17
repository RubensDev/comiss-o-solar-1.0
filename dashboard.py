import streamlit as st
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
    f"Função cadastrada: {st.session_state['funcao']}"
)

st.divider()

funcao = st.session_state["funcao"]

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

    st.divider()

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

st.divider()

st.warning("""
⚠️ IMPORTANTE

Os valores apresentados são estimativas.

Os cálculos são realizados com base nas cubagens informadas pelo usuário.

Pode haver pequenas diferenças de centavos devido aos arredondamentos utilizados pela empresa.

Os registros ficam vinculados apenas ao usuário logado.
""")
