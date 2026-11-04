# A regra que disparou

```
Policy name:      Abnormal Data Egress Volume — Peer Group Deviation
Policy type:      Behavior-based (desvio estatístico)
Datasource:       Web Proxy + Cloud Access Security Broker
Entity (EEO):     Usuário
Severity:         High
Risk score:       +70 na entidade usuário

Condição:
    SUM(bytes_out) por accountname em janela de 24h
    > ( mediana do peer group  ×  5 )
    AND SUM(bytes_out) > 1 GB

Peer group:       "Produto — Analistas" (14 membros)
Baseline:         mediana móvel dos últimos 30 dias do peer group
Janela:           24h deslizante
Threshold:        5x a mediana do grupo

Exclusões:
    - accountname LIKE "svc_%"
    - destination em lista de aplicações sancionadas (sanctioned_apps.lst)
```

## Perguntas obrigatórias sobre esta regra

1. **O que ela testou?** Soma de bytes de saída por usuário, comparada ao grupo.
2. **Qual valor satisfez?** 8,4 GB contra mediana de 0,75 GB.
3. **Era isso que ela pretendia pegar?**
4. **Se for FP — dado, regra ou contexto?**

E as perguntas que tornam este caso N4:

5. **"Essa regra soma bytes para onde?"**
   A condição soma **todo** `bytes_out` do usuário na janela, e só depois aplica a exclusão por
   destino sancionado. Pergunte ao analista o que acontece quando tráfego sancionado e não
   sancionado **compartilham o mesmo IP de destino**.

6. **"O baseline dessa regra é válido para esta entidade?"**
   Mediana móvel de 30 dias do peer group. Pergunte: quanto tempo de histórico **esta** pessoa tem
   nesta função? O que muda se ela trocou de função ou voltou de licença? (→ `logica-deteccao.md`,
   "policy comportamental só vale se o baseline valer")

7. **"Score 88, de 15 para 88 em 7 dias — isso veio de uma coisa grave ou de muitas pequenas?"**

8. **"Como você passaria por essa regra?"**
   A regra entrega: janela de 24h deslizante com threshold de 5x → **fracionar** o upload em
   volumes diários abaixo do limite. E a exclusão por destino sancionado → **usar** uma aplicação
   sancionada como intermediária.

## Nota para o mentor

Esta regra tem uma falha real de desenho: ela agrega **antes** de filtrar por destino. Num ambiente
onde CDNs compartilham IP, isso superestima o volume não sancionado. Se o analista não notar, não
aponte — guarde para a discussão de tuning, e pergunte: "essa regra mede o que ela diz medir?"
