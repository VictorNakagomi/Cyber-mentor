# Cyber Mentor

Skill de mentoria socrática para analistas de SOC. Ensina, questiona, conduz caso de incidente
multi-ferramenta e **avalia a explicação falada do analista** para construir um baseline de
competência por eixo ao longo do tempo.

Premissa: quem não consegue explicar um conceito em linguagem de criança não entendeu o conceito.
O ELI5 é ao mesmo tempo ferramenta de ensino e **instrumento de avaliação**.

## Instalação

```powershell
.\scripts\instalar.ps1 -Dados "$HOME\cyber-mentor-dados"
```

Idempotente. Rodar duas vezes não quebra nada: se já estiver instalado do jeito pedido, ele diz e
sai.

| Modo | O que faz | Para quem |
|---|---|---|
| `-Modo Copia` (padrão) | copia o núcleo para a pasta de skills | distribuição: cada máquina com sua cópia |
| `-Modo Junction` | cria link para o núcleo onde ele já está | autoria: uma fonte de verdade só, editável no lugar |

Outros parâmetros: `-Destino` (pasta de skills alvo), `-Force` (substitui instalação existente).

O script verifica no fim que o `SKILL.md` está legível no destino, que as quatro pastas chegaram,
se o Python existe, e avisa se o pacote contém gabaritos.

### "Instalar para todo o ambiente"

**Não existe pasta de skills no nível da máquina.** O Claude Code procura em:

| Local | Alcance |
|---|---|
| `~/.claude/skills/cyber-mentor/` | todas as sessões **daquele usuário**, em qualquer pasta |
| `<projeto>/.claude/skills/cyber-mentor/` | só naquele projeto |

Então cobrir um parque significa **rodar o instalador no contexto de cada usuário** — logon script,
GPO, Intune, ou à mão. Não há atalho de máquina única.

Para implantação em escala, o instalador foi feito para rodar sem interação:

```powershell
# a partir do pacote já extraído em um share
& "\\share\soc\cyber-mentor\scripts\instalar.ps1" -Dados "$HOME\cyber-mentor-dados" -Force
```

Ele sai com código 1 em qualquer falha (origem inválida, destino ocupado sem `-Force`, estrutura
incompleta), o que serve de condição de sucesso para a ferramenta de implantação.

## Distribuição

```powershell
.\scripts\empacotar.ps1 -Modo Mentoria      # completo, com gabaritos
.\scripts\empacotar.ps1 -Modo SelfService   # sem os gabaritos
```

**São dois pacotes diferentes por desenho, não por conveniência.** O núcleo contém os
`gabarito-raciocinio.md` — as respostas. Quando você conduz, é a sua ferramenta de comparação. No
self-service, o analista é aluno e mentor ao mesmo tempo, e o gabarito na mesma pasta é a resposta
da prova ao lado da prova.

O que o self-service perde é menos do que parece: a condução usa `caso.md`, `regra.md` e
`evidencias/`, e **a avaliação do áudio usa a rubrica, não o gabarito** (a dimensão 3 se apoia no
campo `armadilha` do frontmatter do caso). Perde-se só a comparação final de caminho.

Os blocos `NOTAS PARA O MENTOR` dentro das evidências **continuam** nos dois pacotes, porque o
Claude precisa deles para conduzir. São dicas de condução, não gabarito — mas é bom saber que estão
lá, em vez de descobrir quando um analista citar uma delas numa sessão.

Em qualquer modo o empacotador **aborta** se achar dado de analista (`baseline.json`, `baseline.md`,
`sessoes/`, `avaliacoes/`) dentro do núcleo.

### Do outro lado

```powershell
Expand-Archive "cyber-mentor-selfservice-<data>.zip" -DestinationPath "$env:TEMP\cyber-mentor\"
& "$env:TEMP\cyber-mentor\scripts\instalar.ps1" -Dados "$HOME\cyber-mentor-dados"
# abrir sessão NOVA do Claude Code, e então:
& "$HOME\.claude\skills\cyber-mentor\scripts\novo-analista.ps1" -Nome <nome>
```

Pré-requisito: **Python** apenas para o `recalcular_baseline.py`. Sem Python todos os modos
funcionam; só o baseline automático fica indisponível.

### Onde ficam os dados

Resolvidos nesta ordem, pelo `SKILL.md` e pelos dois scripts:

1. variável de ambiente `CYBER_MENTOR_DADOS`
2. `<diretório atual>/dados-analistas`, se existir
3. `<pasta do núcleo>/../dados-analistas`

```powershell
# recomendado ao distribuir: cada analista aponta a sua
$env:CYBER_MENTOR_DADOS = 'D:\soc\dados-analistas'

# para tornar permanente
[Environment]::SetEnvironmentVariable('CYBER_MENTOR_DADOS', 'D:\soc\dados-analistas', 'User')
```

Se a resolução cair dentro de `.claude/`, os scripts **abortam** — gravar histórico de analista
dentro da árvore de skills quebraria a separação que permite distribuir o núcleo.

```
Skills/
  cyber-mentor/        <- NÚCLEO: distribuível, igual para todos
  dados-analistas/     <- DADOS: locais, nunca saem da máquina (tem .gitignore)
```

Para distribuir, envie **apenas a pasta `cyber-mentor/`**.

## Primeiro uso

```powershell
# 1. criar a pasta de dados do analista
.\cyber-mentor\scripts\novo-analista.ps1 -Nome victor

# 2. preencher dados-analistas\victor\perfil.md
#    a tabela de stack calibra a matriz de competências e os casos

# 3. pedir a autoavaliação inicial (dentro do perfil.md) ANTES da primeira avaliação
#    comparar isso com o baseline real depois de 5 avaliações é o melhor dado de calibração

# 4. rodar o primeiro caso
#    cenarios\001-powershell-codificado-financeiro
```

## Os cinco modos

| Modo | Pedido típico | Pontua? |
|---|---|---|
| `estudo` | "quero estudar DNS tunneling" | não |
| `caso` | "quero treinar um caso" | não |
| `eli5` | "explica como se eu fosse criança" | não |
| `avaliar` | analista entrega transcrição de áudio | **sim — único que move o nível** |
| `baseline` | "como estou?" / "o que estudar?" | não |

## O ciclo completo

```
estudo ou caso  →  analista grava áudio explicando  →  transcrição em
avaliacoes/entrada/  →  modo `avaliar` aplica a rubrica  →
avaliacoes/pontuadas/  →  recalcular_baseline.py  →  baseline.json + .md
```

## Avaliação por áudio

O modo `avaliar` lê um arquivo em `dados-analistas/<nome>/avaliacoes/entrada/` no formato de
`templates/avaliacao-entrada.md`.

**O canal de origem é irrelevante para a avaliação.** Hoje o analista grava e cola a transcrição
(Win+H no Windows, celular, Teams). Amanhã um bot de Telegram ou WhatsApp pode escrever no mesmo
formato, e nenhuma linha da rubrica muda. É esse contrato que faz a integração futura custar pouco.

Nota sobre o bot: skill não roda sozinha — ela existe quando alguém abre uma sessão. Um bot precisa
de processo vivo (servidor, n8n, script de polling) que receba o áudio, transcreva e grave o arquivo
nesta pasta. O contrato já está pronto para isso.

## A rubrica, em uma tela

**Portão** — correção técnica. Erro factual que invalida a conclusão: a avaliação **não conta**.
Não é nota zero; não pontua, não sobe, não desce.

**4 dimensões**, 0–4 cada:
1. Rigor epistêmico — separa evidência / inferência / suposição
2. Arquitetura do raciocínio — cadeia sem salto + alcance (`micro` ou `micro→macro`)
3. Hipóteses alternativas — considerou e descartou, ou travou na primeira
4. Comunicação (ELI5) — a criança entenderia

**Progressão:** `≤5→N1 · 6-8→N2 · 9-11→N3 · 12-14→N4 · 15-16 com Comunicação=4→N5`
Nível sobe só com **2 avaliações consecutivas** na faixa. Nunca desce por avaliação ruim — mas
**expira em 90 dias** e vira `não verificado`.

## Scripts

```powershell
.\scripts\novo-analista.ps1 -Nome <nome>              # cria pasta de dados
python .\scripts\recalcular_baseline.py <nome>        # baseline.json + baseline.md
python .\scripts\recalcular_baseline.py --time        # consolidado do time
```

O baseline **nunca é escrito à mão**: é derivado das avaliações pontuadas, para ser auditável.
Toda nota rastreia para um arquivo em `avaliacoes/pontuadas/`.

## Cenários

| ID | Título | Nível | Ensina |
|---|---|---|---|
| 001 | PowerShell codificado em estação do financeiro | N3 | lógica de detecção, cegueira de EDR em servidor, fuso em timeline, criticidade por urgência |
| 002 | Volume anormal de upload em colaborador em desligamento | N4 | pivô por IP de CDN, baseline comportamental contaminado, data events de nuvem desabilitados |

Cada cenário tem **armadilha plantada** — sem red herring a dimensão 3 da rubrica não é mensurável.

### Convenção dos logs sintéticos

Os logs dos cenários são inventados, e o repositório mantém uma regra: **nenhum IP roteável e
nenhum domínio registrado**. Endereços externos usam as faixas de documentação da RFC 5737
(`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`); e-mails e hosts internos usam os TLDs
reservados da RFC 2606 (`.example`).

O motivo é prático: material de treino em repositório público entra em scraper de IOC. Rotular
faixa de terceiro como C2 faz alguém bloquear netblock alheio por causa de um exercício.

A distribuição dos IPs entre `/24` diferentes **também é desenho**. No cenário 001 o C2 e o destino
legítimo estão cada um na sua faixa, porque a ligação entre os indicadores tem que ser estabelecida
pelo comportamento. Se tudo cair no mesmo `/24`, a correlação vem de graça e o cenário perde o
exercício. Ao criar cenário novo, escolha a faixa pelo **papel** do host, não pela ordem.

Para criar um novo cenário, use `templates/caso.md`. Estrutura obrigatória:
`caso.md` (minuto zero) + `regra.md` (a lógica da detecção) + `evidencias/` (liberadas uma por vez)
+ `evidencias/_indisponivel.md` (a cegueira proposital) + `gabarito-raciocinio.md` (o caminho, não
a resposta).

## Securonix

O eixo `siem-query` ensina a **pedagogia** da query: que hipótese ela testa, que campo comprova, o
que um resultado vazio prova. **A sintaxe de Spotter não vive aqui** — acione a skill
`securonix-spotter`, para não defasar em dois lugares.

Os logs dos cenários usam campos normalizados Securonix. Cada tenant tem parser próprio por
datasource: **confirme os campos no seu ambiente** antes de ensinar como verdade.

## As regras duras

Estão em `SKILL.md` e valem em todos os modos. As três que mais mudam o resultado:

- Nunca responder pergunta que o analista não tentou. Máximo 2 dicas.
- Nunca dar ELI5 antes de ele tentar a versão técnica.
- Nunca aceitar criticidade herdada da severidade do alerta.

## Outros modelos e outros harnesses

O conteúdo é markdown, então viaja. **O que não viaja é o harness** — e é o harness que faz a
skill funcionar, não o modelo. Regras por alvo, os dois eixos (capacidade do ambiente × adesão do
modelo) e o protocolo de validação estão em `references/portabilidade.md`.

O `AGENTS.md` na raiz é o arquivo de descoberta para Cursor, Codex CLI e afins. Para ferramenta que
lê outro nome (`.clinerules`, `GEMINI.md`, `.github/copilot-instructions.md`), copie o conteúdo
dele — são ~15 linhas, não vale abstrair.

### Validar

```powershell
python .\scripts\validar_portabilidade.py                      # no núcleo de autoria
python .\scripts\validar_portabilidade.py --modo selfservice   # no PACOTE extraído
```

**O modo `selfservice` roda no pacote extraído, não no núcleo.** No núcleo ele sempre reprova, e
deve: o núcleo tem os gabaritos. Rodá-lo aqui serve só para provar que a guarda funciona.

Isso valida **estrutura**. Não valida comportamento, e a diferença importa: um pacote que passa
100% pode ser inútil no alvo, porque as regras socráticas dependem de o modelo obedecer instrução
negativa sob pressão. Para isso existem as **8 sondas** de `references/portabilidade.md`, com
`templates/conformidade.md` para registrar o resultado.

Corte: falha na sonda P3 tira o modo `caso`; falha na P6 tira o `avaliar` — e com ele o único modo
que move o nível. Avaliação em ambiente não validado contamina o baseline de forma permanente,
porque a nota fica gravada.
