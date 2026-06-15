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
    f"Usuário: {st.session_state['nome']}"
)

funcao = st.session_state["funcao"]

cubos = st.number_input(
    "📦 Cubagem",
    min_value=0.0,
    step=0.01
)

clientes = st.number_input(
    "👥 Clientes Entregues",
    min_value=0
)

if st.button("💰 Calcular Comissão"):

    if funcao == "Auxiliar":

        valor_cubos = cubos * 0.019
        valor_clientes = clientes * 0.21

    else:

        valor_cubos = cubos * 0.038
        valor_clientes = clientes * 0.43

    comissao = valor_cubos + valor_clientes

    st.success(
        f"🏆 Comissão estimada: R$ {comissao:.2f}"
    )

    st.write(f"📦 Cubagem: {cubos:.2f}")
    st.write(f"👥 Clientes: {clientes}")
    st.write(f"💰 Valor Cubagem: R$ {valor_cubos:.2f}")
    st.write(f"💰 Valor Clientes: R$ {valor_clientes:.2f}")
    st.write(f"🏆 Comissão Total: R$ {comissao:.2f}")

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
            cubos,
            clientes,
            comissao
        )
    )

    conn.commit()

    st.info(
        "Registro salvo no histórico."
    )

st.warning("""
⚠️ IMPORTANTE

Os valores apresentados são estimativas.

Os cálculos são realizados com base nas cubagens informadas pelo usuário.

Pode haver diferenças em relação aos valores oficiais da empresa.
""")