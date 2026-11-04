# Correlação e timeline

## Timeline não é lista de alertas

O erro mais comum: o analista cola os alertas em ordem de chegada e chama de timeline. Timeline é
**reconstrução causal** — cada linha precisa responder *como o atacante chegou nela a partir da
anterior*. Se duas linhas vizinhas não têm ligação causal, falta uma linha no meio, e essa lacuna é
o resultado mais valioso do exercício.

Regra: **toda timeline entregue com lacuna nomeada vale mais que timeline fechada sem lacuna.**

## Pivôs — e a confiança de cada um

Pivô é o campo que liga um log de uma ferramenta ao log de outra. Nem todo pivô vale o mesmo.

| Pivô | Confiança | Por que falha |
|---|---|---|
| Hash de arquivo | Alta | só falha se o arquivo foi recompilado (então o hash muda e você perde o rastro, não erra o elo) |
| Usuário + host + janela | Alta | contas de serviço e sessões compartilhadas quebram |
| ID de sessão / correlação | Alta | existe em poucas fontes; quando existe, é o melhor pivô |
| Nome de host | Média | renomeação, duplicata, nome curto vs. FQDN |
| IP interno | **Baixa** | DHCP e NAT: o mesmo IP é outra máquina depois do lease. **Nunca pivote por IP interno sem janela de tempo** |
| IP externo | Baixa a média | CDN e cloud compartilham IP entre milhares de serviços legítimos |
| Timestamp sozinho | **Baixa** | correlação por "aconteceu junto" é a principal fonte de falsa causalidade |

Pergunta obrigatória sempre que o analista pivotar: **"esse pivô é confiável? dois eventos com esse
mesmo valor são necessariamente a mesma coisa?"**

## O problema dos relógios

É aqui que timelines mentem — e o analista júnior nunca desconfia.

**1. Três tempos diferentes, e eles divergem.** No Securonix: `eventtime` (quando ocorreu na fonte),
`collectiontimestamp` (quando o SIEM recebeu), `publishedtime`. Ordenar por `collectiontimestamp` é
ordenar pela fila do coletor, não pelo ataque. Um host com coletor atrasado aparece "depois" de
eventos que vieram antes dele.

**2. Fuso e normalização.** Fonte em horário local, SIEM em UTC, analista lendo em BRT. Três horas
de diferença põem o logon antes do e-mail que o causou — e aí a conclusão inverte.

**3. Clock skew.** Host com relógio errado produz evento com timestamp impossível. Se um evento
aparece **antes** do que o causou, a primeira hipótese é relógio, não viagem no tempo.

**4. Granularidade diferente.** EDR registra em milissegundos; firewall agrega sessão em janela de
minutos; NetFlow amostra. Colocar os três na mesma linha do tempo sem anotar a granularidade cria
precisão falsa.

**5. Tempo de log vs. tempo de evento.** Log de fim de sessão carrega o horário do fim, mas o evento
*começou* antes. Sessão de 3 horas registrada às 18:00 começou às 15:00.

Perguntas de mentor:
- "Esses dois eventos estão na ordem que o relógio diz, ou na ordem que a causa diz?"
- "Que fuso está nesse campo? Como você confirmou?"
- "Esse timestamp é de quando aconteceu ou de quando chegou?"

## Ordem temporal não é ordem causal

Duas coisas distintas, e o analista funde as duas:

- **Depois** significa só que o relógio é maior.
- **Por causa de** exige mecanismo: o evento A produziu o estado que tornou B possível.

Teste: "me explica o mecanismo que liga A a B". Se ele não consegue nomear o mecanismo, não é
causalidade — é vizinhança temporal, e vizinhança temporal é o motor dos falsos positivos de
correlação.

## Método: âncora, trás, frente

Toda investigação começa num evento só — a âncora (normalmente o alerta). Dali, duas direções:

```
            ← PRA TRÁS                ÂNCORA                 PRA FRENTE →
      como entrou? quem é paciente     o alerta         o que fez com o que
      zero? qual o acesso inicial?                      conseguiu? persistiu?
                                                        moveu? levou algo?
```

**Pra trás** responde escopo e causa raiz. Para o negócio, é o que fecha o incidente.
**Pra frente** responde impacto e urgência. Para o turno, é o que define a ação agora.

Erro de júnior: só ir pra frente, porque é o que o alerta mostra. Resultado: contém o host errado e
o atacante volta pela mesma porta na semana seguinte.

Ordem de pergunta recomendada:
1. "Qual o seu evento âncora, e por que esse?"
2. "O que **tem** que ter acontecido antes disso ser possível?" — raciocínio por pré-requisito, não
   por busca cega.
3. "Que fonte provaria esse passo anterior? Ela existe aqui?" → cruza com `telemetria.md`.
4. "E depois disso, o que o atacante **ganhou**? O que isso permite?"
5. "Qual o maior buraco da sua timeline agora?"

## Formato obrigatório de timeline

Exija esta tabela antes de aceitar qualquer conclusão. As duas últimas colunas são o aprendizado:

| # | Horário (fuso) | Fonte | Evento | Pivô que liga ao anterior | Evid./Infer. | Confiança |
|---|---|---|---|---|---|---|
| 1 | 2026-10-20 14:02 UTC | Proxy | `host.example` acessado por `jsilva` | — (âncora) | Evidência | Alta |
| 2 | 14:02:11 UTC | EDR | `chrome.exe` → `powershell.exe` | host + janela 30s | Evidência | Alta |
| 3 | ~14:05 | — | **LACUNA**: como obteve credencial | — | — | — |
| 4 | 14:38 UTC | AD `4769` | TGS para `CIFS/srv-fin01` | `accountname` | Inferência | Média |

Regras do formato:
- Lacuna é **linha**, não omissão. Timeline sem linha de lacuna é timeline que esconde buraco.
- Coluna `Evid./Infer.` força o rigor epistêmico que a rubrica mede.
- Horário aproximado leva `~`, e isso precisa aparecer.

## Correlacionar fontes diferentes — o roteiro

Para cada hipótese, três fontes independentes, em papéis diferentes:

1. **Fonte que origina** — onde o comportamento nasce (EDR, e-mail, sign-in).
2. **Fonte que confirma** — vê o mesmo fato por outro ângulo (proxy, firewall, DNS).
3. **Fonte que contextualiza** — diz se é normal (baseline, CMDB, histórico do usuário).

Uma hipótese sustentada por uma fonte só é inferência, por mais forte que pareça. Uma hipótese
sustentada por três fontes que **dependem da mesma coleta** também é uma fonte só — e essa confusão
é sutil: proxy, firewall e NetFlow do mesmo link não são três testemunhas independentes do conteúdo,
porque nenhum deles vê conteúdo.

Pergunta de mentor: **"suas três fontes são independentes, ou são três ângulos do mesmo olho?"**

## Exercícios

1. Dois eventos, um com `eventtime` de 14:00 e `collectiontimestamp` de 14:40; outro com
   `eventtime` 14:20 e `collectiontimestamp` 14:25. Qual aconteceu primeiro, e qual você veria
   primeiro na tela?
2. Você liga dois eventos pelo IP `10.20.30.40`, com 6 horas de diferença. Que pergunta você precisa
   responder antes de aceitar esse elo?
3. Monte a timeline de um phishing com clique, só com estas fontes: e-mail gateway, proxy, EDR. Onde
   fica a lacuna inevitável, e qual fonte a fecharia?
4. Um evento de EDR aparece 3 minutos **antes** do e-mail que supostamente o causou. Liste três
   explicações, em ordem de probabilidade.
