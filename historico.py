import streamlit as st
import pandas as pd
from banco import conn, cursor

st.title("📋 Meu Histórico")

if not st.session_state.get("logado"):

    st.warning(
        "Faça login para acessar seu histórico."
    )

    st.stop()

# ======================
# FILTRO POR MÊS
# ======================

mes = st.selectbox(
    "📅 Filtrar por mês",
    [
        "Todos",
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12"
    ]
)

cursor.execute(
    """
    SELECT
        id,
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

    dados_filtrados = []

    for linha in dados:

        id_lancamento = linha[0]
        data = linha[1]

        if mes == "Todos":

            dados_filtrados.append(linha)

        else:

            if data[3:5] == mes:

                dados_filtrados.append(linha)

    if dados_filtrados:

        df = pd.DataFrame(
            dados_filtrados,
            columns=[
                "ID",
                "Data",
                "Cubagem",
                "Clientes",
                "Comissão"
            ]
        )

        df["Cubagem"] = df["Cubagem"].round(2)
        df["Comissão"] = df["Comissão"].round(2)

        st.dataframe(
            df,
            use_container_width=True
        )

        total_mes = df["Comissão"].sum()

        st.success(
            f"💰 Total das Comissões: R$ {total_mes:.2f}"
        )

        st.divider()

        st.subheader("✏️ Editar Data")

        id_editar = st.selectbox(
            "Selecione o ID",
            df["ID"]
        )

        nova_data = st.text_input(
            "Nova data (dd/mm/aaaa)"
        )

        if st.button("Salvar Nova Data"):

            cursor.execute(
                """
                UPDATE lancamentos
                SET data=?
                WHERE id=?
                """,
                (
                    nova_data,
                    int(id_editar)
                )
            )

            conn.commit()

            st.success(
                "Data atualizada com sucesso!"
            )

            st.rerun()

        st.divider()

        st.subheader("🗑️ Excluir Lançamento")

        id_excluir = st.selectbox(
            "Escolha o lançamento",
            df["ID"],
            key="excluir"
        )

        if st.button("Excluir Lançamento"):

            cursor.execute(
                """
                DELETE FROM lancamentos
                WHERE id=?
                """,
                (
                    int(id_excluir),
                )
            )

            conn.commit()

            st.success(
                "Lançamento excluído!"
            )

            st.rerun()

    else:

        st.warning(
            "Nenhum lançamento encontrado neste mês."
        )

else:

    st.warning(
        "Você ainda não possui lançamentos."
    )
