import streamlit as st
import pandas as pd
from banco import conn, cursor

st.title("👑 Painel Administrativo")

cursor.execute("SELECT COUNT(*) FROM usuarios")
total_usuarios = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM lancamentos")
total_lancamentos = cursor.fetchone()[0]

cursor.execute("""
SELECT COALESCE(SUM(comissao),0)
FROM lancamentos
""")
total_comissao = cursor.fetchone()[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Usuários",
        total_usuarios
    )

with col2:
    st.metric(
        "📊 Lançamentos",
        total_lancamentos
    )

with col3:
    st.metric(
        "💰 Comissão Total",
        f"R$ {total_comissao:.2f}"
    )

st.divider()

cursor.execute("""
SELECT
u.nome,
u.usuario,
u.funcao
FROM usuarios u
ORDER BY u.nome
""")

usuarios = cursor.fetchall()

if usuarios:

    df = pd.DataFrame(
        usuarios,
        columns=[
            "Nome",
            "Usuário",
            "Função"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

st.divider()

st.subheader("📋 Todos os Lançamentos")

cursor.execute("""
SELECT
u.nome,
l.data,
l.cubos,
l.clientes,
l.comissao
FROM lancamentos l
JOIN usuarios u
ON l.usuario_id = u.id
ORDER BY l.id DESC
""")

dados = cursor.fetchall()

if dados:

    df2 = pd.DataFrame(
        dados,
        columns=[
            "Nome",
            "Data",
            "Cubos",
            "Clientes",
            "Comissão"
        ]
    )

    st.dataframe(
        df2,
        use_container_width=True
    )

st.success(
    "Painel exclusivo do administrador Rubens"
)