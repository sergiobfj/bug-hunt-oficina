"""SECCO Internal — API do sistema interno."""

import os
import secrets

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.staticfiles import StaticFiles

from db import get_connection, init_db

app = FastAPI(title="SECCO Internal")

init_db()

ADMIN_EMAIL = "admin@secco.com"
ADMIN_PASSWORD = "admin123"

# token -> id do usuário logado
SESSIONS = {}


def novo_token(user_id):
    token = secrets.token_hex(16)
    SESSIONS[token] = user_id
    return token


def get_user_from_token(authorization):
    """Descobre qual usuário está por trás do header Authorization."""
    if not authorization:
        return None

    token = authorization.replace("Bearer ", "")
    user_id = SESSIONS.get(token)

    if not user_id:
        return None

    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    con.close()

    if row is None:
        return None

    return dict(row)


def processar(data):
    email = data["email"]
    senha = data["password"]

    print("LOGIN:", email, senha)

    if email == ADMIN_EMAIL and senha == ADMIN_PASSWORD:
        t = novo_token(1)
        return {"token": t, "user": {"id": 1, "name": "Admin", "role": "admin"}}

    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    x = cur.fetchone()
    con.close()

    if x is None:
        return {"error": "Email não cadastrado"}
    else:
        if x["status"] == "blocked":
            return {"error": "Usuário bloqueado"}
        else:
            if x["password"] == senha:
                a = dict(x)
                t = novo_token(a["id"])
                return {"token": t, "user": a}
            else:
                return {"error": "Senha incorreta"}


@app.post("/api/login")
def login(data: dict):
    try:
        return processar(data)
    except Exception:
        return {"error": "erro"}


@app.post("/api/logout")
def logout(authorization: str = Header(None)):
    if authorization:
        SESSIONS.pop(authorization.replace("Bearer ", ""), None)
    return {"ok": True}


@app.get("/api/me")
def me(authorization: str = Header(None)):
    user = get_user_from_token(authorization)

    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado")

    return {"user": user}


@app.get("/api/users")
def users(q: str = "", limit: int = Query(20, le=100), authorization: str = Header(None)):
    user = get_user_from_token(authorization)

    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado")

    con = get_connection()
    cur = con.cursor()

    pattern = "%" + q + "%"
    cur.execute(
        "SELECT * FROM users WHERE name LIKE ? OR email LIKE ? LIMIT ?",
        (pattern, pattern, limit),
    )

    rows = cur.fetchall()
    con.close()

    lista = []
    for r in rows:
        lista.append(dict(r))

    return {"users": lista}


@app.get("/api/users/{user_id}")
def user_detail(user_id: int, authorization: str = Header(None)):
    user = get_user_from_token(authorization)

    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado")

    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    con.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return dict(row)


@app.get("/api/admin/stats")
def admin_stats(authorization: str = Header(None)):
    u = get_user_from_token(authorization)

    if not u:
        raise HTTPException(status_code=401, detail="Não autenticado")

    if u["role"]:
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "SELECT COUNT(*) AS total,"
            " SUM(status = 'active') AS ativos,"
            " SUM(role = 'admin') AS admins"
            " FROM users"
        )
        row = cur.fetchone()
        con.close()

        return {"total_users": row["total"], "active_users": row["ativos"], "admins": row["admins"]}

    raise HTTPException(status_code=403, detail="Acesso negado")


# O frontend estático é servido pela própria API para facilitar o setup local.
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")