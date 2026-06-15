import streamlit as st

st.set_page_config(
    page_title="Comissão Solar Pro",
    page_icon="🚚",
    layout="wide"
)

menu = st.sidebar.selectbox(
    "Menu",
    [
        "🏠 Início",
        "🔐 Login",
        "📊 Minha Comissão",
        "📅 Meu Histórico"
    ]
)

if menu == "🏠 Início":

    st.title("🚚 Comissão Solar Pro")

    st.subheader(
        "Sistema de Controle de Cubagem e Comissão"
    )

    st.write(
        """
        Bem-vindo ao sistema.

        Cada usuário possui acesso apenas aos próprios dados.

        Faça login para utilizar o sistema.
        """
    )

elif menu == "🔐 Login":

    exec(open("login.py", encoding="utf-8").read())

elif menu == "📊 Minha Comissão":

    exec(open("dashboard.py", encoding="utf-8").read())

elif menu == "📅 Meu Histórico":

    exec(open("historico.py", encoding="utf-8").read())