import streamlit as st
import pandas as pd
from banco import cursor

st.title("📅 Meu Histórico")

if not st.session_state.get("logado"):

    st.warning(
        "Faça login para acessar seu histórico."
    )

    st.stop()

cursor.execute(
    """
    SELECT
        data,
        cubos,
        clientes,
        comissao
    FROM lancamentos
    WHERE usuario_id = ?
    ORDER BY id DESC
    """,
    (
        st.session_state["id_usuario"],
    )
)

dados = cursor.fetchall()

if dados:

    df = pd.DataFrame(
        dados,
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

else:

    st.warning(
        "Você ainda não possui lançamentos."
    )