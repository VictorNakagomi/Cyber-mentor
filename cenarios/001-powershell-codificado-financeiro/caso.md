---
id: 001-powershell-codificado-financeiro
titulo: PowerShell codificado em estação do financeiro
eixos: [logica-deteccao, telemetria, correlacao-timeline, criticidade, endpoint]
nivel_alvo: N3
tecnicas_attack: [T1566.001, T1059.001, T1071.001, T1105]
fontes_disponiveis: ["Endpoint Management Systems", "Web Proxy", "DNS", "Next Generation Firewall", "Microsoft Windows", "Email Gateway"]
fontes_ausentes: ["EDR no SRV-FIN-02", "Inspeção TLS no proxy", "DLP em compartilhamento interno"]
armadilha: sim
duracao_estimada: 40min
---

# PowerShell codificado em estação do financeiro

> **Para o mentor:** entregue APENAS este arquivo e `regra.md`. Nada de `evidencias/`.
> Libere evidência uma por vez, só quando o analista pedir **aquela** evidência e disser **que
> hipótese ela testa**. Pedido sem hipótese volta com: "o que você espera encontrar aí?"

## Minuto zero

```
Securonix — Violation
Policy:        Encoded PowerShell Command Execution
Entity:        WKS-FIN-0455 (host)
Account:       jsilva
Event time:    2026-10-20 14:02:47 BRT
Risk score:    jsilva — 65 (era 20 há 24h)
Severity:      Medium
```

É isso. Não há descrição, não há veredito, não há narrativa.

## Contexto do ambiente

Dados do CMDB. Como qualquer CMDB, podem estar desatualizados — confirmar o dono do ativo faz parte
do exercício de criticidade.

| Ativo | Função | Dono | Criticidade declarada |
|---|---|---|---|
| WKS-FIN-0455 | Estação de trabalho | jsilva — Analista de Contas a Pagar | Média |
| SRV-FIN-02 | File server do financeiro | TI — Infraestrutura | Alta |
| SRV-DC-01 | Controlador de domínio | TI — Infraestrutura | Crítica |

Informação adicional do RH, disponível se o analista perguntar pelo usuário:
jsilva tem acesso ao compartilhamento `\\SRV-FIN-02\pagamentos` e opera o portal bancário.

## Escopo de telemetria

**Fontes integradas:** Endpoint Management Systems (EDR, em estações), Web Proxy (sem inspeção
TLS), DNS, Next Generation Firewall, Microsoft Windows (DCs e servidores), Email Gateway.

**Fontes NÃO integradas** — não revele no início:
- EDR **não está instalado em servidores**, incluindo SRV-FIN-02
- Proxy **sem inspeção TLS**: não há payload, só host de destino e volume
- DLP não monitora compartilhamento interno

Quando ele pedir uma dessas, não diga "não existe". Pergunte:
1. "Que ferramenta geraria esse log?"
2. "Ela está no escopo deste ambiente?"

Só então mostre `evidencias/_indisponivel.md`.

## Evidências disponíveis sob pedido

| Arquivo | O que é | Libere quando ele pedir por… |
|---|---|---|
| `01-securonix-violation.json` | o evento da violação, campos normalizados | detalhe do alerta |
| `02-edr-arvore-processos.json` | árvore de processos no host | o que rodou no endpoint |
| `03-proxy.csv` | log de proxy do usuário na janela | navegação, download |
| `04-dns.log` | queries do host | resolução de domínio, C2 |
| `05-ad-4769.csv` | tickets Kerberos de serviço | acesso a compartilhamento |
| `06-firewall.csv` | sessões de saída do host | conexão externa, volume |
| `07-email-gateway.csv` | e-mails recebidos pelo usuário | vetor inicial, phishing |
| `08-itsm-mudanca.txt` | janela de manutenção registrada | contexto de TI, autorização |
| `_indisponivel.md` | o que este ambiente não vê | fonte que não existe aqui |

## O que o analista precisa entregar

1. **Por que a regra disparou** — os sete componentes de `logica-deteccao.md`, a partir de `regra.md`
2. **Classificação**: TP, TPB ou FP, com justificativa
3. **Timeline** no formato de `correlacao-timeline.md`, **com a lacuna como linha**
4. **Criticidade** justificada pelos seis fatores, com o fator dominante nomeado
5. **Próxima ação** e o custo dela — quem para de trabalhar
6. **O que ele ainda não sabe**

## Pontos de parada obrigatórios

- **Quando ele ler `08-itsm-mudanca.txt`.** É a armadilha. Se ele caminhar para TPB, não corrija:
  pergunte "que horário é a janela, e que horário é o evento?" e deixe ele mesmo achar.
- **Quando ele afirmar exfiltração a partir do proxy.** Pergunte: "o proxy vê conteúdo aqui?"
- **Quando ele pedir EDR do SRV-FIN-02.** É o momento de ensinar cegueira de telemetria.
- **Quando ele der a criticidade.** Se vier "média porque a regra é média", é a regra dura nº 8.
