# A regra que disparou

Entregue junto com `caso.md`. O analista precisa destrinchar isto **antes** de opinar sobre o
alerta — são os sete componentes de `references/logica-deteccao.md`.

```
Policy name:      Encoded PowerShell Command Execution
Policy type:      Rules-based (determinística)
Datasource:       Endpoint Management Systems
Entity (EEO):     Host
Severity:         Medium
Risk score:       +45 na entidade usuário

Condição:
    rg_functionality = "Endpoint Management Systems"
    AND processname CONTAINS "powershell"
    AND ( commandline CONTAINS "-enc"
       OR commandline CONTAINS "-EncodedCommand"
       OR commandline CONTAINS "-e " )
    AND commandline NOT CONTAINS "SOE-Baseline-Config"

Threshold:        1 ocorrência
Janela:           imediata (por evento)
Baseline:         nenhum — regra determinística, não comportamental

Exclusões:
    - accountname LIKE "svc_%"
    - devicehostname LIKE "SRV-BUILD-%"
    - commandline CONTAINS "SOE-Baseline-Config"
```

## Perguntas que o mentor faz sobre a regra

Não entregue respostas. Estas perguntas valem mais que o caso:

1. **O que exatamente essa regra testou?** Diga a condição em português.
2. **Qual campo deste evento satisfez a condição?** O valor concreto.
3. **Este é o comportamento que a regra pretendia pegar, ou ela pegou outra coisa por tabela?**
4. **Se for falso positivo, o problema está no dado, na regra ou no contexto?**

E a pergunta avançada, que é a que mais ensina:

5. **"Como você passaria por essa regra sem ela disparar?"**

   O analista deve chegar sozinho a pelo menos três caminhos. A regra entrega todos eles de graça:
   `-e ` com espaço não pega `-e` no fim da linha; a exclusão por `svc_%` é um presente para quem
   consegue agir como conta de serviço; e qualquer linha que contenha a string `SOE-Baseline-Config`
   é ignorada **em qualquer posição** — inclusive dentro de um comentário colado no comando.

6. **Threshold 1 e janela imediata** — qual o efeito disso no volume da fila? E o que isso diz sobre
   a intenção de quem escreveu a regra?

7. **A regra é determinística, não comportamental.** Que consequência isso tem para a *confiança*
   do alerta — e, portanto, para a criticidade? (→ `criticidade.md`, fator 4)

## Nota para o mentor

Esta regra tem uma falha real de escrita: `commandline CONTAINS "-e "` é largo demais e vai casar
com qualquer PowerShell que tenha um parâmetro começando por `-e` seguido de espaço (`-ExecutionPolicy`
abreviado, por exemplo). Se o analista não notar, não aponte — guarde para a discussão de tuning no
fim, e pergunte: "essa regra pega mais ou menos do que pretendia?"
