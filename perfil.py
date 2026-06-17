import streamlit as st
from banco import conn, cursor

st.title("👤 Meu Perfil")

if not st.session_state.get("logado"):

    st.warning(
        "Faça login para acessar seu perfil."
    )

    st.stop()

st.success(
    f"👤 Nome: {st.session_state['nome']}"
)

st.info(
    f"🔐 Usuário: {st.session_state['usuario']}"
)

st.info(
    f"🚚 Função: {st.session_state['funcao']}"
)

st.divider()

st.subheader("🔑 Alterar Senha")

senha_atual = st.text_input(
    "Senha Atual",
    type="password"
)

nova_senha = st.text_input(
    "Nova Senha",
    type="password"
)

confirmar_senha = st.text_input(
    "Confirmar Nova Senha",
    type="password"
)

if st.button("Alterar Senha"):

    cursor.execute(
        """
        SELECT senha
        FROM usuarios
        WHERE id=?
        """,
        (
            st.session_state["id_usuario"],
        )
    )

    senha_banco = cursor.fetchone()[0]

    if senha_atual != senha_banco:

        st.error(
            "Senha atual incorreta."
        )

    elif nova_senha != confirmar_senha:

        st.error(
            "As senhas não coincidem."
        )

    elif len(nova_senha) < 6:

        st.error(
            "A senha deve possuir pelo menos 6 caracteres."
        )

    else:

        cursor.execute(
            """
            UPDATE usuarios
            SET senha=?
            WHERE id=?
            """,
            (
                nova_senha,
                st.session_state["id_usuario"]
            )
        )

        conn.commit()

        st.success(
            "Senha alterada com sucesso!"
        )

