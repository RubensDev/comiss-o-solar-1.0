import streamlit as st
import pandas as pd
from banco import conn, cursor

st.title("👑 Painel Administrativo")

# ==========================
# MÉTRICAS GERAIS
# ==========================

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

# ==========================
# USUÁRIOS POR FUNÇÃO
# ==========================

st.subheader("📌 Usuários por Função")

cursor.execute("""
SELECT funcao, COUNT(*)
FROM usuarios
GROUP BY funcao
""")

funcoes = cursor.fetchall()

if funcoes:

    df_funcoes = pd.DataFrame(
        funcoes,
        columns=[
            "Função",
            "Quantidade"
        ]
    )

    st.dataframe(
        df_funcoes,
        use_container_width=True
    )

st.divider()

# ==========================
# PESQUISAR USUÁRIO
# ==========================

st.subheader("🔍 Pesquisar Usuário")

pesquisa = st.text_input(
    "Digite nome ou usuário"
)

cursor.execute("""
SELECT
nome,
usuario,
funcao
FROM usuarios
ORDER BY nome
""")

usuarios = cursor.fetchall()

if pesquisa:

    usuarios = [
        u for u in usuarios
        if pesquisa.lower() in u[0].lower()
        or pesquisa.lower() in u[1].lower()
    ]

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

# ==========================
# RANKING DE COMISSÕES
# ==========================

st.subheader("🏆 Ranking de Ganhos")

cursor.execute("""
SELECT
u.nome,
ROUND(COALESCE(SUM(l.comissao),0),2)
FROM usuarios u
LEFT JOIN lancamentos l
ON u.id = l.usuario_id
GROUP BY u.id
ORDER BY SUM(l.comissao) DESC
""")

ranking = cursor.fetchall()

if ranking:

    ranking_df = pd.DataFrame(
        ranking,
        columns=[
            "Usuário",
            "Total Comissão"
        ]
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

st.divider()

# ==========================
# RESETAR SENHA
# ==========================

st.subheader("🔑 Resetar Senha")

cursor.execute("""
SELECT usuario
FROM usuarios
ORDER BY usuario
""")

lista_usuarios = [
    linha[0]
    for linha in cursor.fetchall()
]

usuario_reset = st.selectbox(
    "Selecione o usuário",
    lista_usuarios,
    key="reset"
)

nova_senha = st.text_input(
    "Nova senha",
    type="password"
)

if st.button("Resetar Senha"):

    cursor.execute(
        """
        UPDATE usuarios
        SET senha=?
        WHERE usuario=?
        """,
        (
            nova_senha,
            usuario_reset
        )
    )

    conn.commit()

    st.success(
        "Senha alterada com sucesso."
    )

st.divider()

# ==========================
# EXCLUIR USUÁRIO
# ==========================

st.subheader("🗑️ Excluir Usuário")

usuarios_excluir = [
    u for u in lista_usuarios
    if u != "Rubeensadm"
]

usuario_excluir = st.selectbox(
    "Usuário",
    usuarios_excluir,
    key="delete"
)

if st.button("Excluir Usuário"):

    cursor.execute(
        """
        SELECT id
        FROM usuarios
        WHERE usuario=?
        """,
        (
            usuario_excluir,
        )
    )

    usuario_id = cursor.fetchone()[0]

    cursor.execute(
        """
        DELETE FROM lancamentos
        WHERE usuario_id=?
        """,
        (
            usuario_id,
        )
    )

    cursor.execute(
        """
        DELETE FROM usuarios
        WHERE id=?
        """,
        (
            usuario_id,
        )
    )

    conn.commit()

    st.success(
        "Usuário removido com sucesso."
    )

    st.rerun()

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
            "Cubagem",
            "Clientes",
            "Comissão"
        ]
    )

    st.dataframe(
        df2,
        use_container_width=True
    )

st.success(
    "Sistema Administrativo Online"
)
st.divider()

st.subheader("🔍 Diagnóstico do Banco")

cursor.execute("""
SELECT
id,
nome,
usuario
FROM usuarios
""")

usuarios_debug = cursor.fetchall()

st.write(usuarios_debug)
