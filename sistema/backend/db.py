"""Banco de dados do SECCO Internal (SQLite)."""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "secco.db")


def get_connection():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


USERS = [
    ("Ana Ribeiro", "ana@exemplo.com", "ana123", "admin", "Tecnologia", "active"),
    ("Bruno Carvalho", "bruno@exemplo.com", "bruno123", "manager", "Operações", "active"),
    ("Carla Menezes", "carla@exemplo.com", "carla123", "user", "Produto", "active"),
    ("Diego Almeida", "diego@exemplo.com", "diego123", "user", "Tecnologia", "active"),
    ("Elisa Nunes", "elisa@exemplo.com", "elisa123", "user", "Financeiro", "blocked"),
    ("Felipe Souza", "felipe@exemplo.com", "felipe123", "manager", "Comercial", "active"),
    ("Gabriela Lima", "gabriela@exemplo.com", "gabriela123", "user", "Produto", "pending"),
]


def init_db():
    """Cria a tabela e popula com os usuários de demonstração."""
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT,
            status TEXT NOT NULL
        )
        """
    )

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            """
            INSERT INTO users (name, email, password, role, department, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            USERS,
        )
        con.commit()
        print("Banco criado com", len(USERS), "usuários")

    con.close()
