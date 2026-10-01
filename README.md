# SECCO Bug Hunt & Code Review

Oficina de **análise crítica de código** da [SECCO](https://seccolab.com.br) para
os alunos de Ciência da Computação da Unifavip Wyden, na Semana de TI.

Ministrada por **Gabriel Lemos** e **Sergio Barbosa**.

> ## O código funciona. Mas ele está realmente bom?

---

## ⚠️ Aviso

**O sistema em `sistema/` tem falhas de segurança propositais.**
Use **só em `localhost`**, para fins educacionais. **Nunca faça deploy público.**

Todos os dados são fictícios. O sistema não acessa nada externo e usa só um banco
SQLite local.

---

## Estrutura

```
├── README.md            você está aqui
├── GUIA_ALUNO.md        o que vamos ver na oficina + checklist de code review
└── sistema/
    ├── backend/
    │   ├── main.py      ← a API. É aqui que estão os problemas.
    │   └── db.py        cria o banco SQLite com os usuários de exemplo
    ├── frontend/        a tela: HTML + CSS + JavaScript puro
    │   ├── index.html       login
    │   ├── dashboard.html   perfil
    │   ├── users.html       lista e busca de usuários
    │   ├── admin.html       área administrativa
    │   ├── app.js           funções comuns (chamar a API, topo da página)
    │   ├── styles.css       visual da SECCO
    │   └── fonts/           Space Grotesk e Manrope, servidas localmente
    └── requirements.txt
```

## Como rodar

Requisito: **Python 3.10+**.

```bash
cd sistema
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

Acesse **http://localhost:8000** e entre com `ana@exemplo.com` / `ana123`.
As outras contas estão no [GUIA_ALUNO.md](GUIA_ALUNO.md#rodando-na-sua-máquina-opcional).

---

<p align="center">
  <sub>SECCO INTERNAL · Bug Hunt Lab · Semana de TI Unifavip Wyden</sub>
</p>
