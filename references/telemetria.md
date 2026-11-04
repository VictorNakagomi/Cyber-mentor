# Telemetria — o que cada ferramenta vê, e o que ela é cega para ver

A lacuna mais comum do L1/L2 não é teoria: é não saber **o que cada ferramenta consegue provar**.
O analista sem letramento em telemetria faz duas coisas erradas o dia inteiro:

1. **Pede prova a quem não pode dar** — "pede no firewall o que o usuário baixou".
2. **Aceita como prova o que é só indício** — "o proxy mostra conexão pro IP, então exfiltrou".

Este eixo (`telemetria`) é pré-requisito dos outros dois (`correlacao-timeline`, `criticidade`).

## As três perguntas de telemetria

Use sempre nessa ordem, para qualquer afirmação do analista:

1. **Que ferramenta geraria o log que prova isso?**
2. **Essa ferramenta consegue ver isso?** O que ela não vê?
3. **Tem algo que essa fonte *parece* provar, mas não prova?**

A pergunta 3 é a que ensina. As duas primeiras testam conhecimento; a terceira testa ceticismo.

## Matriz de cobertura e cegueira

A terceira coluna é a mais importante da skill. Use-a para montar pergunta, não para entregar
resposta.

### Rede

| Ferramenta | Vê | Não vê | Parece ver, mas não vê |
|---|---|---|---|
| Firewall / NGFW | 5-tupla, ação allow/deny, bytes, duração, zona | conteúdo, usuário (sem integração de identidade) | `allow` **não** prova que a conexão foi estabelecida — prova que a política permitiu. `deny` não prova ausência de tráfego: pode ter saído por outro caminho |
| Proxy / SWG | host de destino, método, user-agent, categoria, volume, usuário autenticado | payload sob TLS sem interceptação; tráfego que não passa pelo proxy | com TLS vê o `CONNECT host` e o volume, **não a URL completa**. Um GET de 2 KB e um POST de 2 GB para o mesmo host são a mesma linha se você só olhar o host |
| DNS (servidor / PDNS) | query, tipo, cliente, às vezes a resposta | o que aconteceu depois da resolução | resolução **não é** conexão. E a ausência de query não prova ausência de acesso: pode ter vindo do cache, de `hosts`, ou de DNS externo direto |
| NetFlow / IPFIX | quem falou com quem, volume, duração, periodicidade | qualquer conteúdo | ótimo para provar **padrão** (beaconing); péssimo para provar **o quê**. Volume alto não é exfiltração: pode ser backup |
| IDS / IPS | assinatura casada, direção, payload parcial | tráfego cifrado; o que não tem assinatura | em modo detect **não bloqueou**. Alerta de IDS não significa host comprometido: significa pacote visto |
| VPN | sessão, usuário, IP atribuído, duração | o que o usuário fez dentro da sessão | o IP atribuído muda de pessoa ao longo do dia: pivô por IP sem janela de tempo liga gente errada |

### Endpoint

| Ferramenta | Vê | Não vê | Parece ver, mas não vê |
|---|---|---|---|
| EDR / XDR | árvore de processos, linha de comando, arquivo, rede por processo, persistência | hosts **sem agente** — o ponto cego mais caro de todos | se o agente foi instalado **depois** do comprometimento, não há histórico. Ausência de detecção em janela anterior ao deploy não é evidência de nada |
| AV tradicional | assinatura casada, arquivo em quarentena | comportamento sem assinatura | "limpo" só significa "nada conhecido casou". Diz respeito ao banco de assinaturas, não ao host |
| Windows Event Log | logon, criação de conta, serviço, política, acesso a objeto | o que o usuário fez dentro da sessão | `4624` prova que houve logon, **não** o que foi feito depois. O `Logon Type` muda tudo: 3 = rede, 10 = RDP, 2 = interativo local |
| Sysmon | criação de processo com hash, conexão, carregamento de DLL, criação de arquivo | o que não está na config do Sysmon | a cobertura é **a config**, não o produto. Dois hosts com Sysmon podem ter telemetria completamente diferente |

### Identidade

| Ferramenta | Vê | Não vê | Parece ver, mas não vê |
|---|---|---|---|
| AD / Controlador de domínio | `4768` (TGT), `4769` (TGS), `4624`, `4625`, `4740` | o que o ticket abriu depois | `4769` para um serviço **não** prova acesso bem-sucedido ao recurso — prova que o ticket foi emitido |
| Entra ID / sign-in logs | sign-in, IP, dispositivo, MFA, conditional access, risco | uso de token já emitido | sign-in `success` não exclui roubo de token: replay de token pode não gerar sign-in novo. Ausência de sign-in suspeito não é ausência de acesso |
| PAM / cofre | checkout de credencial, sessão privilegiada | uso de credencial que não passou pelo cofre | prova quem **pegou** a chave, não quem a usou |

### Dados e aplicação

| Ferramenta | Vê | Não vê | Parece ver, mas não vê |
|---|---|---|---|
| Email gateway | envelope, remetente, anexo escaneado, URL reescrita, veredito | o que o usuário fez depois de receber | entregue **não** é lido, e lido não é clicado. O clique só aparece no proxy ou na URL reescrita |
| DLP | movimentação no canal monitorado, política violada | canal não monitorado: pendrive sem agente, foto da tela, app pessoal | "nenhum alerta de DLP" cobre só os canais configurados |
| WAF | requisição HTTP, regra casada, ação | o que a aplicação fez com a requisição | bloqueio não prova que o ataque falhou em todos os caminhos; e em modo detection não bloqueou nada |
| CASB | uso de SaaS sancionado, compartilhamento | SaaS fora do catálogo | cobertura depende de integração por API **ou** de inline — e as duas veem coisas diferentes |

### Cloud

| Ferramenta | Vê | Não vê | Parece ver, mas não vê |
|---|---|---|---|
| CloudTrail / Azure Activity | chamadas de API do **plano de controle** | acesso a dados, por padrão | este é o erro mais caro da nuvem: leitura de objeto em bucket é **data event**, e data event normalmente **não está habilitado**. "Não tem log de download" quase nunca significa "não houve download" |
| Logs de fluxo (VPC/NSG) | 5-tupla e volume dentro da nuvem | conteúdo; e tráfego que não cruza a interface logada | amostragem e agregação por janela mascaram picos curtos |
| IAM / Access Analyzer | permissão concedida, política, exposição | se a permissão foi usada | permissão perigosa não é incidente; **uso** dela é |

### Contexto e meta

| Ferramenta | Vê | Não vê | Parece ver, mas não vê |
|---|---|---|---|
| Scanner de vulnerabilidade | exposição potencial **no momento do scan** | exploração | vulnerável não é explorado, e "não vulnerável" é uma foto de ontem |
| CMDB / inventário de ativos | dono, criticidade declarada, ambiente | realidade | é a fonte mais desatualizada do parque, e é a que você usa para julgar criticidade. Sempre confirme o dono |
| Threat intel | reputação, contexto de IOC, TTP conhecido | o seu ambiente | "IP malicioso" com confiança baixa e idade de 2 anos é ruído. Sempre pergunte: qual a fonte, qual a data, qual a confiança |
| SIEM (Securonix) | o que foi coletado, parseado e retido | tudo o resto | o SIEM não é fonte: é mesa. Ele só tem o que alguém mandou pra ele, no formato que o parser entendeu |

## Ausência de log não é ausência de evento

Quando o analista disser "não tem log disso", exija que ele escolha entre as quatro causas — porque
cada uma leva a uma ação diferente:

1. **Não coletado** — a fonte existe, ninguém integrou. → ação: pedir onboarding da fonte.
2. **Não parseado** — chegou ao SIEM como texto cru, o campo não foi mapeado. → ação: olhar o
   `rawevent` antes de concluir. Esta causa é invisível em busca por campo normalizado.
3. **Fora da retenção** — existiu e expirou. → ação: buscar na fonte original, não no SIEM.
4. **Filtrado** — exclusão de regra, allowlist, ou amostragem. → ação: olhar a exclusão.

Pergunta de ouro para o analista: **"isso não existe, ou você não achou?"**

## Campos normalizados Securonix

Vocabulário de pivô mais usado. Trate como ponto de partida: **cada tenant tem parser próprio por
datasource, então confirme os campos no seu ambiente antes de ensinar como verdade.**

| Família | Campos |
|---|---|
| Tempo | `eventtime` (quando ocorreu), `collectiontimestamp` (quando chegou), `publishedtime` |
| Fonte | `rg_functionality`, `rg_vendor`, `rg_name`, `tenantname` |
| Identidade | `accountname`, `userid`, `employeeid`, `email` |
| Rede | `sourceaddress`, `sourceport`, `destinationaddress`, `destinationport`, `destinationhostname` |
| Host | `devicehostname`, `deviceaddress` |
| Processo | `processname`, `parentprocessname`, `commandline` |
| Arquivo | `filename`, `filepath`, `filehash`, `filesize` |
| Ação | `transactionstring`, `categoryobject`, `categorybehavior`, `categoryseverity` |
| Cru | `message`, `rawevent` |

`rg_functionality` é o eixo de telemetria dentro do SIEM: ele diz **que tipo de olho** gerou aquele
evento ("Web Proxy", "Next Generation Firewall", "Endpoint Management Systems", "Data Loss
Prevention"). Ensinar o analista a pensar primeiro em `rg_functionality` e só depois em campo é
ensinar telemetria antes de query.

**A sintaxe de busca não vive aqui** — acione a skill `securonix-spotter`.

## Exercícios de telemetria

Sem caso, só com pergunta. Funcionam em 5 minutos de turno:

1. "Quero provar que o usuário baixou um arquivo de 400 MB de um site novo. Que fontes provam isso,
   e em que ordem você pediria?"
2. "O proxy mostra 2 GB para um host desconhecido. O que isso ainda **não** prova?"
3. "O EDR não mostra nada nesse host. Liste três razões diferentes para isso, e o que cada uma
   mudaria na sua conclusão."
4. "Cliente diz que ninguém leu o arquivo no bucket. Como você verifica — e por que a resposta
   provavelmente é 'não sei'?"
5. "Você tem só NetFlow. Que tipo de ataque você ainda consegue detectar, e qual você nunca verá?"
