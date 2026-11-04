# O que este ambiente NÃO vê

> **Mostre este arquivo somente depois** de o analista pedir uma dessas fontes **e** responder:
> 1. "Que ferramenta geraria esse log?"
> 2. "Ela está no escopo deste ambiente?"
>
> Entregar isto cedo mata o aprendizado mais importante do caso.

| O analista vai querer | Por que não existe | Qual das 4 causas |
|---|---|---|
| EDR no SRV-RH-01 e SRV-FIN-02 | EDR licenciado só para estações | **não coletado** |
| Payload das conexões HTTPS | proxy sem inspeção TLS | **não coletado** |
| Que arquivos foram lidos no `\\SRV-RH-01` | sem auditoria de acesso a objeto no servidor, sem DLP interno | **não coletado** |
| Comando PowerShell completo decodificado | EDR trunca `commandline` em 260 caracteres | **não coletado** (limite do produto) |
| Conteúdo do anexo `NFe_884521.html` | gateway não retém anexo, só hash | **fora da retenção** |
| Prova de que jsilva clicou | nenhuma ferramenta registra o clique: a URL estava dentro do HTML, não no corpo do e-mail | **não coletado** |
| Logs de proxy antes de 13:58 | retenção de 30 dias existe, mas só foi exportada a janela do incidente | disponível se pedir |

## As quatro causas de ausência

Exija que o analista escolha uma para cada "não tem log" — cada uma leva a uma ação diferente:

1. **Não coletado** — a fonte existe, ninguém integrou → pedir onboarding
2. **Não parseado** — chegou cru, campo não mapeado → olhar o `rawevent`
3. **Fora da retenção** — existiu e expirou → buscar na fonte original
4. **Filtrado** — exclusão, allowlist, amostragem → olhar a exclusão

## A conversa que vale mais que o caso

Depois de mostrar isto, faça as três perguntas:

1. **"Com essa cegueira, o que você consegue afirmar com confiança 4?"**
   (Resposta honesta: houve transferência de 1,26 MB do SRV-RH-01 para a estação. Não se sabe
   o quê, nem se foi lido com sucesso.)

2. **"Qual integração você pediria amanhã para não ficar cego de novo?"**
   Força o analista a pensar como engenheiro de detecção, não só como operador. Prioridade
   defensável: auditoria de acesso a objeto nos file servers, porque é a lacuna que impede
   responder "o que vazou" — a única pergunta que o negócio faz.

3. **"E o que você escreve no ticket sobre o que não sabe?"**
   Analista N4 documenta a cegueira. Analista N2 omite e deixa o próximo turno descobrir sozinho.
