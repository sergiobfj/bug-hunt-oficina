# Gabarito — Bug Hunt & Code Review

Aqui está o backend **depois das 10 correções** feitas ao vivo na oficina.
Compare com `sistema/backend/` para ver o que mudou em cada item.

| #  | Problema                                    | O que a correção faz |
| -- | ------------------------------------------- | -------------------- |
| 1  | Senha do admin escrita no código            | Remove o login "especial": todo login passa pelo banco. |
| 2  | Senha aparecendo no log                     | O log guarda só o email. |
| 3  | Nomes ruins e escadinha de `if`             | `authenticate_user`, nomes claros e retorno antecipado. |
| 4  | Entrada sem validação e `except` genérico   | Schema do Pydantic (`LoginRequest`): falta de campo vira 422. |
| 5  | "Sucesso" quando o login falha              | Falha responde 401 ou 403 com `HTTPException`. |
| 6  | Mensagens que entregam informação           | Mesma mensagem para email inexistente e senha errada. |
| 7  | Usuário `pending` consegue entrar           | Só `active` entra (`!= "active"`). |
| 8  | Senha guardada como texto                   | Hash com bcrypt (`db.py`: `hash_password` e `verify_password`). |
| 9  | A senha vai junto nas respostas             | `public_user` devolve só os campos de `PUBLIC_FIELDS`. |
| 10 | Qualquer um entra no admin                  | Só `role == "admin"` vê as métricas. |

## Como rodar o gabarito

1. Copie `main.py` e `db.py` desta pasta por cima de `sistema/backend/`.
2. Apague `sistema/backend/secco.db`. Ele será recriado com as senhas em hash.
3. Suba de novo:

```bash
cd sistema/backend
uvicorn main:app --reload
```

As contas são as mesmas do [GUIA_ALUNO.md](../GUIA_ALUNO.md#rodando-na-sua-máquina-opcional).
Agora a Gabriela (`pending`) e a Elisa (`blocked`) não entram, e a Carla (`user`) não acessa a Administração.

> Dá para melhorar mais? Sempre. Code review não termina, ele reduz riscos.
