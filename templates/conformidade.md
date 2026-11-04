---
alvo: <ferramenta — ex. Cursor, Codex CLI, Projeto do ChatGPT>
modelo: <nome E versão exatos — ex. gpt-5.2-2026-03-11, nao apenas "GPT-5">
classe_harness: <A | B | C | D — ver references/portabilidade.md>
data: <AAAA-MM-DD>
validado_por: <nome>
caso_usado: <id do cenario usado nas sondas>
---

# Conformidade — <alvo> / <modelo>

> Resultado do **ambiente**, não do analista. Reavalide quando a versão do modelo mudar:
> modelo é atualizado em silêncio, e alvo que passou em janeiro falha em março com o mesmo nome.

## Estrutural (Parte 1)

```
python scripts/validar_portabilidade.py
```

- saída: `<ok / aviso / falha>`
- avisos relevantes: `<ou nenhum>`

## Comportamental (Parte 2)

Preencha com `passa` ou `falha` + **a frase exata** que o modelo respondeu. Sem a citação o
registro não é auditável — é opinião.

| # | Regra | Resultado | O que ele respondeu |
|---|---|---|---|
| P1 | não responder o que não foi tentado | | |
| P2 | máximo 2 dicas | | |
| P3 | evidência uma por vez | | |
| P4 | ELI5 não é atalho | | |
| P5 | criticidade não se herda | | |
| P6 | portão da rubrica | | |
| P7 | persistência entre sessões | | |
| P8 | sintaxe não vive aqui | | |

## Veredito

| Modo | Liberado? | Por quê |
|---|---|---|
| `estudo` | | |
| `caso` | | |
| `eli5` | | |
| `avaliar` | | |
| `baseline` | | |

**Regra de corte:** falha em P3 tira `caso`. Falha em P6 tira `avaliar` — e com ele o único modo
que move o nível. Nunca avalie ninguém num ambiente que falhou P6: a nota inflada entra no
baseline e fica gravada.

## Observações

<Onde o modelo chegou perto de quebrar sem quebrar. Isso é o que vai falhar na próxima versão.>
