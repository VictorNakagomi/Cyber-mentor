# O que este ambiente NÃO vê

> Mostre somente depois de o analista pedir a fonte **e** responder: "que ferramenta geraria esse
> log?" e "ela está no escopo deste ambiente?"

| O analista vai querer | Por que não existe | Causa |
|---|---|---|
| `GetObject` no bucket corporativo | **data events desabilitados** no CloudTrail/trail do bucket | **não coletado** |
| Quais arquivos foram para o SyncDrive Pro | CASB vê aplicação, contagem e volume — não nomes nem conteúdo | **não coletado** |
| DLP no notebook da mrocha | BYOD: sem agente corporativo | **não coletado** |
| Processos e leitura de arquivo no notebook | sem EDR no dispositivo pessoal | **não coletado** |
| Tráfego fora da VPN | proxy só vê o que passa por ele | **não coletado** |
| Conteúdo das sessões TLS | proxy sem inspeção | **não coletado** |

## A conversa que vale mais que o caso

**1. "Com essa cegueira, o que você afirma com confiança 4?"**

Resposta honesta — e é desconfortável:
- 2,07 GB foram para aplicação **não sancionada** (CASB, evidência direta)
- Houve **enumeração** repetida de `exports/` no bucket corporativo (plano de controle)
- A enumeração de 2026-11-05 11:12 UTC precede o primeiro upload em 36 minutos
- **Não se sabe** se algum objeto do bucket foi baixado
- **Não se sabe** o que estava nos 214 + 89 + 31 arquivos enviados

A conclusão "dados do bucket corporativo foram exfiltrados" é **inferência**, não evidência. Forte,
plausível, e ainda assim inferência. Analista que a declara como fato perde a dimensão 1 da rubrica
e, em contexto real, pode sustentar uma ação jurídica sobre dado que não existe.

**2. "Qual integração você pediria amanhã?"**

Prioridade defensável: **habilitar data events** no bucket. É a lacuna que impede responder "o que
vazou" — a única pergunta que o negócio faz. Custa dinheiro em volume de log, e esse trade-off faz
parte da resposta de um N4.

Segunda: política de BYOD com agente, ou proibição de acesso a dado sensível de dispositivo sem
telemetria. Isso é decisão de risco, não de SOC — e saber a diferença também é N4.

**3. "O que você escreve no ticket sobre o que não sabe?"**

Este caso **tem que** ser fechado com a cegueira documentada. Um ticket que diz "sem evidência de
exfiltração de dados do bucket" é tecnicamente verdadeiro e operacionalmente mentiroso: não havia
como haver evidência. A frase correta é "não há telemetria capaz de confirmar ou descartar acesso a
objeto neste bucket".

A diferença entre essas duas frases é a diferença entre N2 e N4.
