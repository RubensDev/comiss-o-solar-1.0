import streamlit as st

st.set_page_config(
    page_title="Comissão Solar Pro",
    page_icon="🚚",
    layout="wide"
)

menu = st.sidebar.selectbox(
    "📌 Menu",
    [
        "🏠 Início",
        "🔐 Login",
        "📊 Minha Comissão",
        "📋 Meu Histórico"
    ]
)

if menu == "🏠 Início":

    st.title("🚚 Comissão Solar Pro")

    st.subheader(
        "Controle de Cubagem e Comissão"
    )

    st.success(
        """
        👋 Bem-vindo ao Comissão Solar Pro.

        Sistema criado para auxiliar motoristas e auxiliares
        no acompanhamento de cubagem, clientes entregues
        e comissão estimada.
        """
    )

    st.markdown("---")

    st.warning(
        """
        ⬅️ PRIMEIRO ACESSO

        Clique na seta ( > ) localizada
        no canto superior esquerdo da tela.

        Depois clique em:

        🔐 Login

        para criar sua conta ou entrar no sistema.
        """
    )

    st.markdown("---")

    st.subheader("📋 Como Utilizar")

    st.write("""
    1️⃣ Clique em 🔐 Login

    2️⃣ Crie sua conta

    3️⃣ Faça login

    4️⃣ Acesse 📊 Minha Comissão

    5️⃣ Informe sua cubagem

    6️⃣ Informe seus clientes

    7️⃣ Calcule sua comissão

    8️⃣ Consulte seus resultados em 📋 Meu Histórico
    """)

    st.markdown("---")

    st.subheader("📦 O que é Cubagem?")

    st.info(
        """
        Cubagem é o volume total informado
        nas entregas realizadas.

        Utilize os valores informados pela empresa
        para calcular sua comissão estimada.
        """
    )

    st.markdown("---")

    st.subheader("🔒 Segurança")

    st.success(
        """
        ✅ Cada usuário possui login próprio

        ✅ Cada usuário vê apenas seus próprios dados

        ✅ Nenhum usuário pode visualizar informações de outro usuário

        ✅ Histórico individual protegido

        ✅ Recuperação de senha disponível
        """
    )

    st.markdown("---")

    st.subheader("⚠️ Aviso")

    st.warning(
        """
        Os valores apresentados são estimativas.

        Os cálculos são realizados com base
        nas informações fornecidas pelo usuário.

        Pode haver pequenas diferenças em relação
        aos valores oficiais da empresa devido
        a arredondamentos ou regras internas.
        """
    )

    st.markdown("---")

    st.success(
        """
        🚀 Desenvolvido por Rubens Miranda
        """
    )

elif menu == "🔐 Login":

    exec(
        open(
            "login.py",
            encoding="utf-8"
        ).read()
    )

elif menu == "📊 Minha Comissão":

    exec(
        open(
            "dashboard.py",
            encoding="utf-8"
        ).read()
    )

elif menu == "📋 Meu Histórico":

    exec(
        open(
            "historico.py",
            encoding="utf-8"
        ).read()
    )
