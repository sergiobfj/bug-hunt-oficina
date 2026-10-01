# Guia do Aluno — Bug Hunt & Code Review

> **O código funciona. Mas ele está realmente bom?**

Hoje você vai ver um sistema que **funciona**: tem login, perfil, lista de
usuários, busca e área de administração. Mesmo assim, ele tem vários problemas.
A gente vai encontrar cada um, explicar por que é um problema e mostrar como
fica o código resolvido.

Você não precisa fazer nada durante a aula além de acompanhar. Se quiser rodar
o sistema na sua máquina, as instruções estão no fim deste guia.

---

## Onde olhar

Quase tudo acontece em **um arquivo**:

```
sistema/backend/main.py
```

É o "backend", a parte que roda no servidor. O `db.py` só cria o banco de
dados, e a pasta `frontend/` é a tela (HTML, CSS e JavaScript puro).

> 💡 **Dica:** muita coisa da aula dá para ver sem ler código. Aperte **F12** no
> navegador, vá na aba **Network (Rede)** e veja o que a API responde de verdade.
> O que a tela esconde, o navegador recebeu mesmo assim.

---

## As 5 perguntas de um code review

Leve essas perguntas para qualquer código que você ler, seu ou de outra pessoa:

1. **Funciona corretamente?**
2. **Funciona com entradas inesperadas?**
3. **É seguro?**
4. **Outro desenvolvedor entenderia?**
5. **Continuaria funcionando em maior escala?**

## As 4 palavras do dia

| Palavra             | O que é                                              |
| ------------------- | ---------------------------------------------------- |
| **Bug**             | O programa faz algo diferente do que deveria.        |
| **Code smell**      | Funciona, mas vai dar dor de cabeça para manter.     |
| **Vulnerabilidade** | Uma brecha que alguém pode explorar.                 |
| **Dívida técnica**  | O atalho de hoje que vira o custo de amanhã.         |

---

## O que vamos ver

Use a coluna da direita para anotar o que achar importante. As linhas são as do
arquivo **antes** das correções: conforme a gente conserta ao vivo, elas mudam de lugar.

### Bloco 1 — O óbvio ⭐

| #  | Problema                          | Onde (`main.py`) | Anotações |
| -- | --------------------------------- | ---------------- | --------- |
| 1  | Senha do admin escrita no código  | linha 15         |           |
| 2  | Senha aparecendo no log           | linha 55         |           |
| 3  | Nomes ruins e escadinha de `if`   | linha 51         |           |

### Bloco 2 — O login ⭐ / ⭐⭐

| #  | Problema                                    | Onde (`main.py`) | Anotações |
| -- | ------------------------------------------- | ---------------- | --------- |
| 4  | Entrada sem validação e erro escondido      | linhas 82–86     |           |
| 5  | Resposta de "sucesso" quando o login falha  | linhas 68–78     |           |
| 6  | Mensagens de erro que entregam informação   | linhas 68–78     |           |
| 7  | Regra de status incompleta                  | linha 70         |           |

### Bloco 3 — Os dados ⭐⭐

| #  | Problema                              | Onde                               | Anotações |
| -- | ------------------------------------- | ---------------------------------- | --------- |
| 8  | Senha guardada como texto             | `db.py` e `main.py` linha 73       |           |
| 9  | Dados demais nas respostas da API     | `main.py` linhas 76, 103, 127, 148 |           |

### Bloco 4 — O acesso ⭐

| #  | Problema                              | Onde (`main.py`) | Anotações |
| -- | ------------------------------------- | ---------------- | --------- |
| 10 | Controle de acesso da área admin      | linha 158        |           |

---

## As regras para levar para a vida

- **Senha, token e segredo não ficam no código e nem no log.**
- **Senha se guarda como hash** (bcrypt), nunca como texto.
- **Não devolva um dado só porque você tem acesso a ele.**
- **Autenticação ≠ Autorização.**
  *Autenticação:* quem é você? *Autorização:* o que você pode fazer?
- **Esconder um dado na tela não é segurança.** Quem decide é o backend.
- **`except Exception` que esconde o erro não resolve o erro.**
- **Liste o que é permitido**, em vez de tentar listar tudo que é proibido.

> **Código funcionar é só o primeiro requisito.**
> Um bom código também precisa ser compreensível, previsível, seguro, testável
> e fácil de manter.

---

## Checklist rápido de code review

Para usar no trabalho, no estágio ou no TCC:

```
LEGIBILIDADE   [ ] Os nomes dizem o que as coisas são?
               [ ] Dá para ler a função sem rolar a tela?
LÓGICA         [ ] A condição representa a regra de negócio de verdade?
ENTRADA        [ ] Dados que vêm de fora são validados?
SEGURANÇA      [ ] Tem senha/segredo no código ou no log?
               [ ] Entrada do usuário chega direto numa query?
               [ ] Cada rota confere QUEM é e O QUE pode?
               [ ] A resposta devolve só o necessário?
ERROS          [ ] O erro é tratado ou só escondido?
               [ ] O status HTTP condiz com o que aconteceu?
BANCO          [ ] Precisa mesmo de SELECT *? Tem paginação?
```

---

## Rodando na sua máquina (opcional)

Precisa de **Python 3.10+**.

```bash
cd sistema
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

Abra **http://localhost:8000**.

| Email                | Senha         | Cargo   | Status  |
| -------------------- | ------------- | ------- | ------- |
| ana@exemplo.com      | `ana123`      | admin   | active  |
| bruno@exemplo.com    | `bruno123`    | manager | active  |
| carla@exemplo.com    | `carla123`    | user    | active  |
| diego@exemplo.com    | `diego123`    | user    | active  |
| elisa@exemplo.com    | `elisa123`    | user    | blocked |
| felipe@exemplo.com   | `felipe123`   | manager | active  |
| gabriela@exemplo.com | `gabriela123` | user    | pending |

> ⚠️ Esse sistema tem falhas de segurança **de propósito**. Use só no seu
> computador (`localhost`) e nunca coloque num servidor público. Todos os dados
> são inventados.
