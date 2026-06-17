import streamlit as st
from banco import conn, cursor

st.title("🔐 Login e Cadastro")

aba1, aba2, aba3 = st.tabs(
    [
        "Entrar",
        "Cadastrar",
        "Esqueci a Senha"
    ]
)

# ======================
# LOGIN
# ======================

with aba1:

    st.subheader("Entrar")

    usuario = st.text_input(
        "Usuário",
        key="login_usuario"
    )

    senha = st.text_input(
        "Senha",
        type="password",
        key="login_senha"
    )

    if st.button(
        "Entrar",
        key="btn_login"
    ):

        cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE usuario=? AND senha=?
            """,
            (usuario, senha)
        )

        usuario_encontrado = cursor.fetchone()

        if usuario_encontrado:

            st.session_state["logado"] = True
            st.session_state["id_usuario"] = usuario_encontrado[0]
            st.session_state["nome"] = usuario_encontrado[1]
            st.session_state["usuario"] = usuario_encontrado[2]
            st.session_state["funcao"] = usuario_encontrado[4]

            if usuario_encontrado[2] == "Rubens01":

                st.session_state["admin"] = True

            else:

                st.session_state["admin"] = False

            st.success(
                f"Bem-vindo, {usuario_encontrado[1]}!"
            )

        else:

            st.error(
                "Usuário ou senha inválidos."
            )
# ======================
# CADASTRO
# ======================

with aba2:

    st.subheader("Cadastrar")

    nome = st.text_input(
        "Nome Completo",
        key="cad_nome"
    )

    novo_usuario = st.text_input(
        "Novo Usuário",
        key="cad_usuario"
    )

    nova_senha = st.text_input(
        "Nova Senha",
        type="password",
        key="cad_senha"
    )

    funcao = st.selectbox(
        "Função",
        ["Auxiliar", "Motorista"],
        key="cad_funcao"
    )

    st.markdown("### 🔑 Recuperação de Senha")

    st.info(
        "Escolha uma palavra secreta. Você usará esta palavra caso esqueça sua senha."
    )

    palavra_secreta = st.text_input(
        "Palavra Secreta",
        key="cad_palavra"
    )

    if st.button(
        "Cadastrar",
        key="btn_cadastro"
    ):

        try:

            cursor.execute(
                """
                INSERT INTO usuarios
                (
                    nome,
                    usuario,
                    senha,
                    funcao,
                    palavra_secreta
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    nome,
                    novo_usuario,
                    nova_senha,
                    funcao,
                    palavra_secreta
                )
            )

            conn.commit()

            st.success(
                "Cadastro realizado com sucesso!"
            )

        except Exception as erro:

            st.error(
                f"Erro: {erro}"
            )

# ======================
# RECUPERAR SENHA
# ======================

with aba3:

    st.subheader("🔑 Recuperar Senha")

    st.info(
        "Digite sua palavra secreta para criar uma nova senha."
    )

    usuario_rec = st.text_input(
        "Usuário",
        key="rec_usuario"
    )

    palavra_rec = st.text_input(
        "Palavra Secreta",
        key="rec_palavra"
    )

    nova_senha_rec = st.text_input(
        "Nova Senha",
        type="password",
        key="rec_senha"
    )

    if st.button(
        "Alterar Senha",
        key="btn_recuperar"
    ):

        cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE usuario=?
            AND palavra_secreta=?
            """,
            (
                usuario_rec,
                palavra_rec
            )
        )

        usuario_ok = cursor.fetchone()

        if usuario_ok:

            cursor.execute(
                """
                UPDATE usuarios
                SET senha=?
                WHERE usuario=?
                """,
                (
                    nova_senha_rec,
                    usuario_rec
                )
            )

            conn.commit()

            st.success(
                "Senha alterada com sucesso!"
            )

        else:

            st.error(
                "Palavra secreta inválida."
            )

# ======================
# LOGOUT
# ======================

st.markdown("---")

if st.session_state.get("logado"):

    st.success(
        f"Logado como: {st.session_state['usuario']}"
    )

    if st.button(
        "🚪 Sair",
        key="btn_logout"
    ):

        st.session_state.clear()

        st.rerun()
