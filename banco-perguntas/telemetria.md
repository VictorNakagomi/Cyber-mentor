# Banco de perguntas — eixo `telemetria`

## Formato (modelo para os outros eixos)

Cada tema é uma **cadeia**, não uma lista. Cada pergunta usa a resposta da anterior, e a ordem segue
os 4 blocos de `references/escada-perguntas.md`. Perguntas soltas não constroem raciocínio.

Para criar o banco de outro eixo, copie esta estrutura:
`Tema → cadeia (4 blocos) → o que cada resposta revela → resgate se travar`.

---

## Tema: o que o proxy prova sobre exfiltração

**OBSERVAR**
1. Você tem uma linha de proxy: 2 GB de saída para um host desconhecido. O que você **vê**, sem
   interpretar?
2. Esse proxy faz inspeção TLS? Como você sabe?

**EXPLICAR**
3. Com TLS e sem inspeção, que campos esse log tem de verdade?
4. Então o que esses 2 GB são — conteúdo, ou medida?

**CORRELACIONAR**
5. Que outra fonte confirmaria o **conteúdo**? Ela existe aqui?
6. Firewall, proxy e NetFlow do mesmo link: são três testemunhas independentes do conteúdo?

**JULGAR**
7. Com o que você tem, qual sua confiança de 0 a 4 de que houve exfiltração de dado corporativo?
8. O que faltaria para ser 4?

*O que a cadeia revela:* a pergunta 6 separa N3 de N4 — quem responde "três fontes confirmam"
não entendeu que nenhuma delas vê conteúdo.

---

## Tema: ausência de log

**OBSERVAR**
1. Você buscou e não achou. Diga a frase exata que você escreveria no ticket.

**EXPLICAR**
2. "Não existe" ou "não achei"? Escolha uma das quatro causas: não coletado, não parseado, fora da
   retenção, filtrado.
3. Como você distinguiria "não parseado" de "não coletado"?

**CORRELACIONAR**
4. Se fosse parser, onde você olharia? (resposta esperada: `rawevent`)
5. Que outra fonte cobriria a mesma pergunta por outro caminho?

**JULGAR**
6. Que conclusão você pode tirar de uma busca vazia? E qual você **não** pode?
7. Como isso muda a criticidade?

*O que a cadeia revela:* viés de ausência (`references/vieses.md`). Analista N2 conclui
"não aconteceu"; N4 conclui "não tenho como saber, e isso é um achado".

---

## Tema: EDR sem agente

**OBSERVAR**
1. O EDR não mostra nada nesse host. Liste três razões diferentes para isso.

**EXPLICAR**
2. Para cada razão, o que muda na sua conclusão?
3. Se o agente foi instalado depois do comprometimento, o que a ausência de detecção prova?

**CORRELACIONAR**
4. Sem EDR nesse servidor, que fontes sobram para saber o que aconteceu nele?
5. Um `4769` para esse servidor prova acesso ao recurso?
6. Uma sessão SMB em `allow` no firewall prova o quê, exatamente?

**JULGAR**
7. Qual a afirmação mais forte que você pode fazer com confiança 4 sobre esse servidor?
8. Que integração você pediria amanhã, e qual o custo dela?

*O que a cadeia revela:* a pergunta 7 é o teste de honestidade epistêmica — e a 8 separa operador
de engenheiro de detecção.

---

## Tema: nuvem e data events

**OBSERVAR**
1. O log de nuvem não tem nenhum `GetObject`. O que isso significa?

**EXPLICAR**
2. Qual a diferença entre plano de controle e plano de dados?
3. `GetObject` é qual dos dois? Ele vem habilitado por padrão?

**CORRELACIONAR**
4. Que evidência de *interesse* o plano de controle ainda entrega? (enumeração)
5. Interesse é o mesmo que acesso?

**JULGAR**
6. Escreva a frase do ticket. Compare: "sem evidência de download" versus "sem telemetria capaz de
   confirmar ou descartar download". Qual é honesta?
7. Qual custa mais: habilitar data events, ou não saber o que vazou?

*O que a cadeia revela:* a pergunta 6 é, sozinha, um bom tema de áudio para avaliação.

---

## Perguntas de resgate (específicas deste eixo)

| Situação | Pergunta |
|---|---|
| afirma que uma ferramenta vê algo que ela não vê | "em que campo desse log isso apareceria?" |
| trata veredito de ferramenta como fato | "o que a ferramenta precisaria ver pra dizer isso? ela vê?" |
| soma volume sem questionar o pivô | "esse número foi composto como?" |
| conclui a partir de busca vazia | "isso não existe, ou você não achou?" |
| pede fonte que não existe no ambiente | "que ferramenta geraria esse log? ela está no escopo?" |
