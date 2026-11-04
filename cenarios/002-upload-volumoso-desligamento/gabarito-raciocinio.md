# Gabarito de raciocínio — 002

> **Não é a resposta. É o caminho esperado.** Compare o caminho, não a conclusão.
> Este caso é N4: ele pune soma ingênua de bytes e premia quem questiona o pivô e o baseline.

## 1. Por que a regra disparou — e o baseline vale?

A regra somou `bytes_out` por usuário em 24h e comparou com 5x a mediana do peer group: 8,4 GB
contra 0,75 GB.

Mas há **dois problemas de validade** que o analista precisa levantar:

**a) O baseline da entidade está contaminado.** mrocha trocou de função em 2026-09-01 e ficou 4
semanas de licença (08/09 a 05/10). Uma policy comportamental exige histórico contínuo; ela tem 65
dias de função nova com um buraco de 4 semanas no meio. O próprio motor sinaliza: *"entidade com
menos de 90 dias de atividade contínua"*.

**b) A regra agrega antes de filtrar.** A condição soma todo o `bytes_out` e só depois aplica a
exclusão por destino sancionado. Num ambiente onde CDN compartilha IP, isso superestima.

**Conclusão de validade:** o *desvio estatístico* é questionável. O *upload para aplicação não
sancionada* é fato independente do baseline. São duas coisas, e separá-las é o centro do caso.

## 2. A armadilha do pivô — quanto foi de verdade

Todos os destinos resolvem para `192.0.2.44`, um IP de CDN compartilhado.

| Pivô usado | Volume calculado | Está certo? |
|---|---|---|
| `destinationaddress` | 8,4 GB | **Não.** Mistura backup corporativo com nuvem pessoal |
| `aplicacao` + `sancionada` | **2,07 GB** não sancionado, 6,95 GB sancionado | Sim |

6,95 GB são do agente `CorpSync`, corporativo e sancionado. O volume realmente relevante é
**2,07 GB** em 334 arquivos.

Isto é a tabela de confiança de pivôs em ação: **IP externo é pivô de confiança baixa**, porque
CDN compartilha IP entre milhares de serviços legítimos.

Erro a pegar: analista que repete os 8,4 GB como fato. Pergunta: "como esse número foi composto?"

## 3. Timeline (fuso unificado em UTC)

CASB e nuvem em UTC; proxy e RH em BRT. Converter é obrigatório.

| # | Horário UTC | Fonte | Evento | Evid./Infer. |
|---|---|---|---|---|
| 1 | 2026-11-03 13:12 | RH | pedido de demissão (10:12 BRT) | Evidência |
| 2 | 2026-11-03 13:40 | Cloud CP | `ListBuckets` + `ListObjectsV2` em `exports/` — 28 min após | Evidência |
| 3 | 2026-11-04 21:02 | Cloud CP | nova enumeração de `exports/` | Evidência |
| 4 | 2026-11-04 22:10 | CASB | 2,85 GB → CorpSync (**sancionado**) | Evidência |
| 5 | 2026-11-05 01:30 | CASB | 3,10 GB → CorpSync (**sancionado**) | Evidência |
| 6 | 2026-11-05 11:12 | Cloud CP | `ListObjectsV2` em `exports/2026/` | Evidência |
| 7 | — | — | **LACUNA: download de objeto. Data events desabilitados.** | — |
| 8 | 2026-11-05 11:48 | CASB | 1,22 GB / 214 arquivos → **SyncDrive Pro (não sancionado)** — 36 min após a enumeração | Evidência |
| 9 | 2026-11-05 14:22 | CASB | 649 MB / 89 arquivos → SyncDrive Pro | Evidência |
| 10 | 2026-11-05 18:55 | CASB | 201 MB / 31 arquivos → SyncDrive Pro | Evidência |
| 11 | — | — | **LACUNA: quais arquivos. CASB não vê nome nem conteúdo.** | — |
| 12 | 2026-11-05 19:40 | Securonix | violação dispara | Evidência |

A sequência **demissão → enumeração → upload pessoal** é o elo mais forte do caso. Mas é **ordem
temporal**, e causalidade exige mecanismo: não há log ligando os arquivos do bucket aos arquivos
enviados. Rotular isso como inferência é obrigatório.

Erros de timeline a pegar:
- não converter fuso e perder a ordem demissão → enumeração
- omitir as linhas 7 e 11
- somar as linhas 4 e 5 ao total "vazado"

## 4. Classificação

**TP — verdadeiro positivo**, com ressalva: o *valor* que disparou a regra está inflado, e o
*desvio comportamental* tem baseline frágil. Mas upload de 2,07 GB para aplicação não sancionada por
colaboradora em aviso prévio, 36 minutos após enumerar o bucket corporativo, é positivo verdadeiro.

Dois erros opostos a pegar:
- **Fechamento prematuro:** "8,4 GB exfiltrados, caso fechado." Não leu o pivô.
- **Descarte excessivo:** "baseline contaminado, é FP." Trocou uma conclusão apressada por outra.
  O baseline frágil derruba o *desvio*, não o *fato* do upload não sancionado.

O segundo erro é mais sofisticado e por isso mais perigoso — e merece a mesma pergunta:
"o que te levou a aceitar isso tão rápido?"

## 5. Criticidade esperada: P2

1. **Ativo** — dados de analytics de produto: propriedade intelectual, não dado regulado. Impacto
   competitivo, não de compliance. Ela vai para empresa do mesmo setor.
2. **Estágio** — Actions on Objective. Não há cadeia de ataque: há abuso de acesso legítimo.
3. **Escopo** — 1 identidade, 334 arquivos, 1 aplicação externa. Escopo **não confirmado**: não se
   sabe se houve outro canal (fora da VPN, o proxy é cego).
4. **Confirmação** — média. O upload é evidência direta; o *conteúdo* é suposição.
5. **Reversibilidade** — **zero**. O dado já está em nuvem de terceiro. Não volta.
6. **Urgência** — média-alta, mas não por causa do que já foi: **o acesso continua ativo e o
   offboarding não foi iniciado**, com 9 dias restantes. O teste de uma hora: em uma hora não muda
   nada; em nove dias, muda muito.

**Fator dominante: reversibilidade combinada com acesso ainda ativo.** Não é o volume, e não é a
severidade da regra.

Erros de criticidade a pegar:
- "High porque a regra é High" → regra dura nº 8
- "Crítica, 8,4 GB vazaram" → inflar por número errado
- "Baixa, saída amigável e termo assinado" → o tom da saída não é evidência de intenção
- "Urgente agora" sem distinguir: o dado já saiu; a urgência é sobre os 9 dias à frente

## 6. Próxima ação e custo

Esperado, em paralelo:
1. **Revogar acesso ao bucket e à VPN agora**; e-mail/Confluence conforme decisão do negócio.
   Custo: ela não documenta as entregas, e o gestor pediu esse acesso.
2. **Habilitar data events** no bucket — não resolve o passado, impede o próximo.
3. **Acionar RH e jurídico** com o que é evidência e o que é inferência, separados.
4. **Iniciar o offboarding**, que é o achado de processo.

A ação mais importante não é técnica: é **documentar a cegueira**. Dizer "sem evidência de
exfiltração do bucket" é tecnicamente verdadeiro e operacionalmente mentiroso — não havia como
haver evidência. A frase certa é "não há telemetria capaz de confirmar ou descartar acesso a objeto
neste bucket".

## 7. Lacunas que devem ir para `lacunas.md`

- [ ] soma volume por IP de destino sem verificar se o IP é compartilhado
- [ ] não questiona validade de baseline em policy comportamental
- [ ] trata ausência de `GetObject` como ausência de download (viés de ausência)
- [ ] conta fontes que compartilham o mesmo caminho como independentes
- [ ] não converte fuso entre CASB/nuvem (UTC) e proxy/RH (BRT)
- [ ] usa contexto humano ("saída amigável") como evidência de intenção
- [ ] herda criticidade da severidade da regra
- [ ] não distingue reversibilidade de urgência

## 8. Tema de áudio sugerido

Eixo **`correlacao-timeline`**, 5–8 min:

> "Explique, como se eu fosse uma criança, por que o número 8,4 GB estava errado, e como você
> descobriu o número certo."

Discrimina bem: exige rigor epistêmico (o que o log prova), arquitetura (a cadeia do pivô),
hipóteses alternativas (o caso tem armadilha) e comunicação (explicar pivô de CDN sem jargão).

Alternativa para eixo `criticidade`:

> "Explique por que um alerta de 8,4 GB virou um caso de 2 GB — e por que ele continua sendo P2
> mesmo assim."
