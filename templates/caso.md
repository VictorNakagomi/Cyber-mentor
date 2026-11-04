---
id: <NNN-slug>
titulo: <título>
eixos: [<eixos exercitados>]
nivel_alvo: <N2|N3|N4>
tecnicas_attack: [<Txxxx.xxx>]
fontes_disponiveis: [<rg_functionality de cada fonte presente>]
fontes_ausentes: [<fontes que o analista vai querer e não existem>]
armadilha: <sim|nao>
duracao_estimada: <ex: 40min>
---

# <título>

> **Para o mentor:** entregue APENAS este arquivo e `regra.md`. Nada de `evidencias/`.
> Libere evidência uma por vez, só quando o analista pedir **aquela** evidência e disser **que
> hipótese ela testa**. Pedido sem hipótese recebe de volta: "o que você espera encontrar aí?"

## Minuto zero

<O que o SOC vê no instante do alerta, e nada mais. Sem conclusão, sem narrativa, sem adjetivo.
Se este bloco der a resposta, o caso está mal escrito.>

## Contexto do ambiente

<Só o que está no CMDB e no inventário — e deixe explícito que esses dados podem estar
desatualizados, porque confirmar o dono do ativo faz parte do exercício de criticidade.>

| Ativo | Função | Dono | Criticidade declarada |
|---|---|---|---|
| | | | |

## Escopo de telemetria

**Fontes integradas:** <liste por `rg_functionality`>

**Fontes NÃO integradas:** <liste — mas NÃO mostre ao analista no início.>

Quando ele pedir uma fonte ausente, não diga "não existe". Pergunte:
1. "Que ferramenta geraria esse log?"
2. "Ela está no escopo deste ambiente?"

Só então mostre `evidencias/_indisponivel.md`. **Cegueira de telemetria se aprende tomando na cara.**

## O que o analista precisa entregar

1. Por que a regra disparou (os sete componentes de `logica-deteccao.md`)
2. Classificação: TP, TPB ou FP — com justificativa
3. Timeline no formato de `correlacao-timeline.md`, **com a lacuna como linha**
4. Criticidade justificada pelos seis fatores de `criticidade.md`, com o fator dominante nomeado
5. Próxima ação e o custo dela
6. O que ele ainda não sabe

## Pontos de parada

<Momentos em que o mentor deve parar e perguntar, mesmo que o analista esteja fluindo. Normalmente:
a primeira conclusão precipitada, e o momento em que ele morde a armadilha.>
