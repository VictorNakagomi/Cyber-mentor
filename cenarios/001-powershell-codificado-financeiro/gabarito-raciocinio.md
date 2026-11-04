# Gabarito de raciocínio — 001

> **Isto não é a resposta do caso. É o caminho esperado.**
> Compare o *caminho* do analista, não a conclusão. Analista que chega à conclusão certa por
> vizinhança temporal pontua menos que analista que para numa conclusão parcial com rigor.
> Não abra este arquivo antes de ele ter entregue timeline e criticidade.

## 1. Por que a regra disparou

| Componente | Resposta esperada |
|---|---|
| Fonte | Endpoint Management Systems (EDR), só em estações |
| Observável | `processname` + `commandline` |
| Condição | `powershell` no nome do processo E `-enc`/`-EncodedCommand`/`-e ` na linha de comando |
| Threshold | 1 ocorrência |
| Janela | imediata, por evento |
| Baseline | nenhum — determinística |
| Exclusão | `svc_%`, `SRV-BUILD-%`, e qualquer linha contendo `SOE-Baseline-Config` |

Campo que satisfez: `commandline` com `-enc`.
A regra pegou o que pretendia pegar. Confiança da detecção: **alta** (determinística, condição
precisa). Isso alimenta o fator 4 da criticidade.

**Bônus de N4:** notar que `-e ` é largo demais e produz FP com `-ExecutionPolicy` abreviado.

## 2. Classificação

**TP — verdadeiro positivo.** Não é TPB e não é FP.

Os dois descartes que precisam aparecer:

- **Não é TPB** pela janela de manutenção: ela é 03:00–05:00, o evento é 14:02:47, ambos em BRT.
- **Não seria nem detectável** pela regra, porque o comando da mudança contém
  `SOE-Baseline-Config`, que está na exclusão. A atividade legítima nunca dispararia.

O segundo descarte é o que separa N3 de N4: exige ter lido a lógica da regra, não só o horário.

## 3. Timeline esperada

Fuso unificado em BRT. O `05-ad-4769.csv` está em **UTC** — converter é obrigatório.

| # | Horário BRT | Fonte | Evento | Pivô | Evid./Infer. | Conf. |
|---|---|---|---|---|---|---|
| 1 | 13:54:12 | Email GW | e-mail com `NFe_884521.html`, DKIM fail, veredito clean | — | Evidência | Alta |
| 2 | **~13:58** | — | **LACUNA: abertura do anexo e clique. Nenhuma fonte registra.** | — | — | — |
| 3 | 13:59:47 | Proxy | `nfe-portal-seguro.com` via chrome.exe, 14 KB | host + user | Evidência | Alta |
| 4 | 14:00:04 | EDR | chrome.exe cria `NFe_884521.zip` (41216 B) | host | Evidência | Alta |
| 5 | 14:00:00 | Firewall | **DENY** SMB para 10.10.5.21 (SRV-RH-01) | host | Evidência | Alta |
| 6 | 14:02:19 | EDR | execução de `NFe_884521.lnk` pelo explorer | host | Evidência | Alta |
| 7 | 14:02:47 | EDR | `cmd.exe` → `powershell.exe -enc` **(âncora do alerta)** | host | Evidência | Alta |
| 8 | 14:02:51 | EDR + Proxy | powershell baixa 284672 B de `cdn-nfe-assets.com` | processo | Evidência | Alta |
| 9 | 14:03:02 | EDR | `rundll32.exe msupdate.dll,Start` | processo pai | Evidência | Alta |
| 10 | 14:03:09+ | EDR/FW/Proxy | beacon para `api-telemetry-sync.com` a cada ~60s | processo | Evidência | Alta |
| 11 | 14:03:40 | EDR | persistência em `HKCU\...\Run\MSUpdateSvc` | processo | Evidência | Alta |
| 12 | 14:35–14:38 | FW + Proxy | 216 KB enviados ao C2 (pico isolado) | host | Evidência | Alta |
| 13 | 14:46:30 | DNS | resolução de `srv-rh-01.corp.example` | host | Evidência | Alta |
| 14 | 14:46:38 | AD 4769 | TGS `CIFS/SRV-RH-01` (17:46:38 **UTC**) — 0 em 30 dias | conta | Evidência | Alta |
| 15 | 14:45 (janela) | Firewall | SMB **ALLOW**: 1,26 MB **recebidos** de SRV-RH-01 | host | Evidência | Alta |
| 16 | — | — | **LACUNA: o que foi lido no SRV-RH-01. Sem EDR, sem auditoria, sem DLP.** | — | — | — |

Erros de timeline que o mentor deve pegar:
- **Não converter UTC** no 4769. Põe o acesso ao RH 3h depois e desconecta do incidente.
- **Ordenar por `collectiontimestamp`.** O evento âncora tem 6m25s de atraso de coleta.
- **Omitir as linhas 2 e 16.** Timeline sem lacuna como linha é timeline que esconde buraco.
- **Tratar a linha 5 (DENY às 14:00) como ruído sem rotular.** Pode ser descoberta de rede do
  Windows, pode ser atividade anterior ao phishing. Não precisa resolver — precisa rotular como
  incerteza aberta.

## 4. O que está provado e o que não está

| Afirmação | Status |
|---|---|
| Houve execução de PowerShell codificado | **Evidência** |
| Houve download de segundo estágio e persistência | **Evidência** |
| Há canal C2 ativo com padrão de máquina | **Evidência** (regularidade + bytes quase idênticos) |
| Houve transferência de 1,26 MB do SRV-RH-01 para a estação | **Evidência** |
| jsilva clicou no anexo | **Inferência** por proximidade temporal — nenhuma fonte prova |
| Os 216 KB enviados ao C2 são dados corporativos | **Inferência** — proxy sem TLS não vê conteúdo |
| O que foi lido no SRV-RH-01 | **Suposição** — não há fonte |
| A conta foi comprometida, não a usuária agiu por conta própria | **Inferência** |

Esta tabela **é** a dimensão 1 da rubrica. Se o analista não a produz espontaneamente, a nota é no
máximo 2.

## 5. Criticidade esperada: P2, caminhando para P1

Justificativa pelos seis fatores:

1. **Ativo** — estação de perfil médio, mas com acesso a `\\SRV-FIN-02\pagamentos` e ao portal
   bancário. O valor está no **alcance**, não no host.
2. **Estágio** — passou de acesso inicial. Há C2, persistência e movimentação para um segundo
   servidor. Não é mais reversível com fechar o navegador.
3. **Escopo** — 1 estação confirmada + 1 servidor tocado. **Escopo não confirmado como pequeno:**
   o C2 está ativo e o beacon continua. "Só um host" aqui é "só um host que eu achei".
4. **Confirmação** — alta. Detecção determinística, cadeia de processos completa, três fontes.
5. **Reversibilidade** — persistência ainda removível; o 1,26 MB já saiu do servidor; os 216 KB já
   saíram da rede e **não voltam**.
6. **Urgência** — alta. O canal está ativo. Em uma hora o atacante pode ter mais credenciais e mais
   servidores. O teste de uma hora falha.

**Fator dominante: urgência**, por canal C2 ativo com persistência. Não é o ativo.

Erros de criticidade a pegar:
- "Média, porque a regra é Medium" → regra dura nº 8, ancoragem pura.
- "Crítica porque tem DC envolvido" → o DC só emitiu ticket; inflar pelo nome do ativo.
- "Baixa porque é só uma estação" → viés de escopo.
- "Alta mas sem urgência" → confundir impacto com urgência; o beacon está vivo.

## 6. Próxima ação e custo

Esperado: **isolar WKS-FIN-0455 agora** (contenção de rede, não desligar — preservar memória),
em paralelo com rotação da credencial de jsilva.

Custo que ele precisa saber nomear: jsilva para de trabalhar; Contas a Pagar pode ter pagamento em
andamento; e desligar em vez de isolar destrói a memória que responderia o que o `msupdate.dll` fazia.

O que **não** pode ficar de fora da ação: o SRV-RH-01 precisa de verificação, mesmo sem EDR.

## 7. Lacunas que devem ir para `lacunas.md`

Marque as que apareceram **neste** analista:

- [ ] não converte fuso antes de montar timeline
- [ ] trata `4769` como prova de acesso ao recurso
- [ ] aceita volume de proxy como prova de exfiltração de conteúdo
- [ ] não distingue "não existe" de "não achei"
- [ ] não lê a lógica da regra antes de classificar TP/TPB/FP
- [ ] herda criticidade da severidade do alerta
- [ ] não nomeia lacuna como linha da timeline
- [ ] confunde urgência com impacto

## 8. Tema de áudio sugerido

Eixo **`telemetria`**, 5–8 min:

> "Explique, como se eu fosse uma criança, o que este ambiente **conseguiu** provar e o que ele foi
> **cego** para provar neste incidente — e por quê."

É o tema que mais discrimina neste caso: exige rigor epistêmico, arquitetura micro→macro e
comunicação ao mesmo tempo. O caso tem armadilha, então a dimensão 3 é avaliável.
