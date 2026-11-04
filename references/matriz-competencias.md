# Matriz de competências

Nível do analista **não é um número só**. "Analista nível 3" não diz onde ele trava. O baseline é
uma matriz: **eixo × nível**, cada eixo avaliado de forma independente.

## Os 5 níveis (iguais para todo eixo)

| Nível | Nome | O que o analista consegue fazer |
|---|---|---|
| N1 | Reconhece | identifica o termo, sabe que existe, não explica |
| N2 | Descreve | explica o que é, com a definição de outra pessoa |
| N3 | Aplica | usa no turno, em caso conhecido, com apoio |
| N4 | Correlaciona | liga a outras fontes e contextos, resolve caso novo sozinho |
| N5 | Ensina | explica a quem não é da área, e sabe onde a própria analogia quebra |

N5 exige `Comunicação = 4` na rubrica. O topo de cada eixo só se alcança ensinando — é a premissa da
skill, não um detalhe.

## Os eixos, em 3 grupos

### Grupo A — Fundamentos técnicos
*O que é a tecnologia e como ela quebra.*

| Eixo | Escopo |
|---|---|
| `redes` | TCP/IP, DNS, HTTP/TLS, proxy, tunelamento, beaconing, exfiltração |
| `endpoint` | processo, árvore de processos, persistência, LOLBin, injeção, serviços |
| `identidade` | AD, Kerberos, NTLM, Entra ID, MFA, token, sessão, privilégio |
| `cloud` | IAM, API, logs de plano de controle, storage público, chave vazada |
| `malware` | família, loader, dropper, C2, ofuscação, comportamento vs. assinatura |

### Grupo B — Prática analítica
*O que separa quem fecha ticket de quem investiga. Núcleo da skill.*

| Eixo | Escopo |
|---|---|
| `telemetria` | que log cada ferramenta entrega, o que ela NÃO vê, o que ela parece ver mas não vê |
| `correlacao-timeline` | pivôs entre fontes, problema de relógio, montar a linha do tempo |
| `logica-deteccao` | por que a regra disparou, anatomia da regra, TP / FP / TP benigno |
| `criticidade` | julgar severidade real, não herdar a do alerta |
| `siem-query` | pedagogia da query: que hipótese testa, que campo comprova, o que vazio prova |

### Grupo C — Processo e ofício

| Eixo | Escopo |
|---|---|
| `processo-ir` | containment, erradicação, recuperação, cadeia de custódia, handoff de turno |
| `threat-intel` | IOC vs. TTP, Pyramid of Pain, atribuição, confiabilidade de fonte |
| `comunicacao` | reportar pra gestão, escrever o caso, explicar sem jargão |

## Formato no `baseline.json`

```json
{
  "analista": "victor",
  "atualizado": "2026-10-29",
  "eixos": {
    "telemetria": {
      "nivel": 3,
      "status": "verificado",
      "ultima_avaliacao": "2026-10-20",
      "expira": "2027-01-18",
      "historico_notas": [10, 11],
      "alcance_tipico": "micro",
      "calibracao_media": 0.8
    }
  },
  "lacunas_abertas": 4,
  "avaliacoes_totais": 7,
  "avaliacoes_portao_fechado": 1
}
```

`status`: `verificado` | `nao_verificado` (passou de 90 dias) | `nunca_avaliado`.

## Como ler a matriz na mentoria

Três padrões que valem intervenção, e são invisíveis se o nível for um número único:

1. **Grupo A alto, Grupo B baixo.** Sabe tecnologia, não sabe investigar. Perfil mais comum de quem
   estudou por certificação. Não ensine mais teoria — dê caso.
2. **`criticidade` abaixo de `logica-deteccao`.** Entende por que a regra disparou mas não sabe o
   quanto importa. Risco direto: escala tudo, ou fecha o que não devia. Trabalhe `criticidade.md`.
3. **`comunicacao` travado em N2–N3 com Grupo A alto.** Sabe e não transmite. Como nível só sobe por
   áudio avaliado, esse analista **estagna em todos os eixos** — a comunicação é gargalo global.
   Trate como prioridade, não como competência secundária.

## Progressão não é linear entre eixos

Não exija que o analista suba todos os eixos junto. Um L2 de SOC bom tem `telemetria` N4 e
`malware` N1, e isso é saudável. O que não é saudável é `criticidade` N1 em quem já opera sozinho.
