import sqlite3

conn = sqlite3.connect(
    "banco.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ==========================
# TABELA DE USUÁRIOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    funcao TEXT NOT NULL,
    palavra_secreta TEXT NOT NULL
)
""")

# ==========================
# TABELA DE LANÇAMENTOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS lancamentos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    data TEXT,
    cubos REAL,
    clientes INTEGER,
    comissao REAL,
    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id)
)
""")

conn.commit()