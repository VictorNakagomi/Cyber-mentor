---
id: 002-upload-volumoso-desligamento
titulo: Volume anormal de upload em colaborador em desligamento
eixos: [correlacao-timeline, logica-deteccao, criticidade, telemetria, cloud]
nivel_alvo: N4
tecnicas_attack: [T1567.002, T1530, T1119]
fontes_disponiveis: ["Web Proxy", "Cloud Access Security Broker", "Cloud Infrastructure", "Data Loss Prevention", "Human Resources"]
fontes_ausentes: ["CloudTrail data events no bucket corporativo", "DLP em dispositivo pessoal (BYOD)", "EDR no notebook (BYOD aprovado)"]
armadilha: sim
duracao_estimada: 50min
---

# Volume anormal de upload em colaborador em desligamento

> **Para o mentor:** entregue APENAS este arquivo e `regra.md`. Libere evidência uma por vez, só
> com hipótese declarada. Este caso é N4: ele pune soma ingênua de bytes e premia quem questiona
> o pivô e o baseline.

## Minuto zero

```
Securonix — Violation
Policy:        Abnormal Data Egress Volume — Peer Group Deviation
Policy type:   Behavior-based
Entity:        mrocha (usuário)
Event time:    2026-11-05 19:40 UTC
Risk score:    mrocha — 88 (era 15 há 7 dias)
Severity:      High
Detalhe:       8.4 GB de upload em 24h — 11,2x a mediana do peer group
```

## Contexto do ambiente

| Entidade | Dado |
|---|---|
| mrocha | Analista de Produto Sr. — mudou de função em 2026-09-01 |
| Dispositivo | Notebook pessoal, BYOD aprovado, **sem EDR corporativo** |
| Acesso | Bucket `s3://corp-produto-analytics` (leitura), Confluence, Jira |
| Ferramenta corporativa | Agente de backup `CorpSync` — faz upload diário para nuvem sancionada |

## Escopo de telemetria

**Fontes integradas:** Web Proxy, CASB, Cloud Infrastructure (plano de controle), DLP (estações
corporativas), RH.

**Fontes NÃO integradas** — não revele no início:
- **CloudTrail data events desabilitados** no bucket corporativo
- DLP não cobre dispositivo pessoal
- Sem EDR no notebook BYOD

## Evidências disponíveis sob pedido

| Arquivo | O que é |
|---|---|
| `01-securonix-violation.json` | o evento da violação e o baseline usado |
| `02-casb-upload.csv` | uploads por destino e aplicação (UTC) |
| `03-proxy.csv` | sessões por host de destino (BRT) |
| `04-cloud-plano-controle.csv` | chamadas de API no bucket corporativo |
| `05-rh-desligamento.txt` | situação funcional da colaboradora |
| `_indisponivel.md` | o que este ambiente não vê |

## O que o analista precisa entregar

1. Por que a regra disparou — e **se o baseline dela é válido**
2. Classificação: TP, TPB ou FP
3. **Quanto foi realmente para destino não sancionado** — com o pivô justificado
4. Timeline com fuso unificado e lacuna como linha
5. Criticidade pelos seis fatores, com o dominante nomeado
6. Próxima ação e custo

## Pontos de parada obrigatórios

- **Quando ele citar os 8,4 GB como fato.** Pergunte como esse número foi composto.
- **Quando ele somar bytes por IP de destino.** É a armadilha principal.
- **Quando ele montar a timeline.** CASB em UTC, proxy em BRT. Se não converter, a conclusão
  sobre motivação inverte.
- **Quando ele afirmar que dados do bucket foram levados.** Pergunte que log prova leitura de
  objeto.
- **Quando ele der a criticidade.** "High porque a regra é High" é a regra dura nº 8.
