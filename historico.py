import streamlit as st
import pandas as pd
from banco import conn, cursor

st.title("📋 Meu Histórico")

if not st.session_state.get("logado"):

    st.warning(
        "Faça login para acessar seu histórico."
    )

    st.stop()

meses = {
    "Janeiro": "01",
    "Fevereiro": "02",
    "Março": "03",
    "Abril": "04",
    "Maio": "05",
    "Junho": "06",
    "Julho": "07",
    "Agosto": "08",
    "Setembro": "09",
    "Outubro": "10",
    "Novembro": "11",
    "Dezembro": "12"
}

mes = st.selectbox(
    "📅 Filtrar por mês",
    ["Todos"] + list(meses.keys())
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

        data = linha[1]

        if mes == "Todos":

            dados_filtrados.append(linha)

        else:

            if data[3:5] == meses[mes]:

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

        cubagem_total = df["Cubagem"].sum()

        clientes_total = df["Clientes"].sum()

        quantidade_lancamentos = len(df)

        st.divider()

        st.subheader("📊 Resumo do Período")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📦 Cubagem Total",
                f"{cubagem_total:.2f}"
            )

            st.metric(
                "👥 Clientes",
                int(clientes_total)
            )

        with col2:

            st.metric(
                "💰 Comissão Total",
                f"R$ {total_mes:.2f}"
            )

            st.metric(
                "📅 Lançamentos",
                quantidade_lancamentos
            )

        st.divider()

        st.success(
            f"💰 Total das Comissões: R$ {total_mes:.2f}"
        )

        st.divider()

        st.subheader("✏️ Editar Lançamento")

        id_editar = st.selectbox(
            "Selecione o ID",
            df["ID"],
            key="editar"
        )

        cursor.execute(
            """
            SELECT cubos, clientes, data
            FROM lancamentos
            WHERE id=?
            """,
            (int(id_editar),)
        )

        registro = cursor.fetchone()

        cubagem_atual = registro[0]
        clientes_atual = registro[1]
        data_atual = registro[2]

        nova_data = st.text_input(
            "Nova Data",
            value=data_atual
        )

        nova_cubagem = st.number_input(
            "Nova Cubagem",
            value=float(cubagem_atual),
            step=0.01
        )

        novos_clientes = st.number_input(
            "Novos Clientes",
            value=int(clientes_atual),
            step=1
        )

        if st.button(
            "Salvar Alterações",
            key="salvar_edicao"
        ):

            funcao = st.session_state["funcao"]

            if funcao == "Auxiliar":

                valor_cubos = nova_cubagem * 0.019
                valor_clientes = novos_clientes * 0.21

            else:

                valor_cubos = nova_cubagem * 0.038
                valor_clientes = novos_clientes * 0.43

            nova_comissao = round(
                valor_cubos + valor_clientes,
                2
            )

            cursor.execute(
                """
                UPDATE lancamentos
                SET
                    data=?,
                    cubos=?,
                    clientes=?,
                    comissao=?
                WHERE id=?
                """,
                (
                    nova_data,
                    nova_cubagem,
                    novos_clientes,
                    nova_comissao,
                    int(id_editar)
                )
            )

            conn.commit()

            st.success(
                "✅ Lançamento atualizado!"
            )

            st.rerun()

        st.divider()

        st.subheader("🗑️ Excluir Lançamento")

        id_excluir = st.selectbox(
            "Escolha o lançamento",
            df["ID"],
            key="excluir"
        )

        if st.button(
            "Excluir Lançamento",
            key="btn_excluir"
        ):

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
                "🗑️ Lançamento excluído!"
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
