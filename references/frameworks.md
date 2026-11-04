# Frameworks — para que serve cada um

Framework não é conteúdo para decorar: é lente. Cada um responde uma pergunta diferente, e o erro do
analista é usar o framework errado para a pergunta que tem.

| Framework | Pergunta que ele responde | Quando NÃO usar |
|---|---|---|
| Kill Chain | em que ponto do roteiro o atacante está? | não serve para ameaça interna nem para abuso de credencial legítima |
| MITRE ATT&CK | que técnica concreta é essa, e o que vem depois dela? | não diz criticidade nem prioridade |
| Diamond Model | o que eu sei e o que me falta sobre este adversário? | não serve para priorizar fila |
| Pyramid of Pain | o que eu bloqueio para doer de verdade? | não serve para investigar um caso único |
| OODA | por que estou perdendo a corrida contra o atacante? | não é método de investigação |

## Kill Chain — onde ele está

Recon → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objective

Uso real: **estágio é fator de criticidade** (→ `criticidade.md`). O mesmo malware em Delivery e em
Actions on Objective tem gravidade completamente diferente.

Limite que o analista precisa saber: a kill chain é linear e a realidade não é. O atacante volta,
repete e pula etapas. E ela não descreve bem o caso mais comum do SOC moderno: credencial válida
usada por quem não devia — não há exploit, não há instalação.

Pergunta: "em que estágio está, e que estágio ele pula se já tem credencial válida?"

## MITRE ATT&CK — o que é e o que vem depois

Táticas (o objetivo) × Técnicas (o como). O valor para o analista não é classificar: é **antecipar**.

```
Identifiquei T1059.001 (PowerShell).
Pergunta certa não é "qual o ID?" — é:
"quem normalmente usa isso logo depois? e o que isso exige que tenha acontecido antes?"
```

Duas armadilhas:
1. **Virar etiquetadeira.** Mapear o alerta para uma técnica e achar que investigou. Mapear é o
   começo.
2. **Confundir técnica com severidade.** ATT&CK não tem nota de gravidade, e com razão: depende do
   ativo.

Uso bom na mentoria: para cada técnica identificada, exija um pré-requisito e uma consequência.
Isso transforma ATT&CK em motor de timeline (→ `correlacao-timeline.md`, raciocínio por
pré-requisito).

## Diamond Model — o que me falta

Quatro vértices: **Adversário · Capacidade · Infraestrutura · Vítima**.

A utilidade está no uso diagnóstico: preencha os vértices que você tem, e os vazios são a sua agenda
de investigação. É o framework que melhor expõe lacuna, porque o vazio é visível.

Pergunta: "quais vértices você tem com evidência, e qual deles você preencheria primeiro?"

## Pyramid of Pain — o que dói no atacante

Do mais fácil de trocar ao mais difícil:

```
Hash de arquivo        trivial de trocar (recompila)
IP                     fácil (muda de VPS)
Domínio                fácil (registra outro)
Artefato de rede/host  trabalhoso
Ferramenta             custoso
TTP                    muito custoso — exige reaprender o ofício
```

Uso: explica por que bloquear hash e IP dá sensação de vitória e nenhuma proteção. E explica a
diferença prática entre IOC e TTP no eixo `threat-intel`.

Pergunta: "você bloqueou o quê? isso custa o que pro atacante — minutos ou meses?"

## OODA — por que estou perdendo

Observe → Orient → Decide → Act. Vale pelo conceito de **velocidade de ciclo**: quem completa o
ciclo mais rápido dita o jogo.

Uso na mentoria: quando o caso se arrasta, pergunte em qual passo o analista está parado. Quase
sempre é Orient — ele tem dado, não tem sentido. E a resposta para travar em Orient não é coletar
mais dado: é formular hipótese.

Pergunta: "você está travado por falta de dado ou por falta de hipótese?"

## Como usar na sessão

- Em `estudo`: um framework por sessão, e sempre aplicado a um caso. Framework sem caso não fixa.
- Em `caso`: nunca comece por framework. Deixe o analista investigar e só no final pergunte "onde
  isso cai no ATT&CK?" — primeiro o raciocínio, depois o vocabulário.
- Em `avaliar`: usar o nome do framework corretamente **não** pontua. Usar a lente para chegar a uma
  conclusão pontua. Analista que fala "isso é TA0008" sem explicar o mecanismo está decorando, e a
  dimensão 2 da rubrica pega isso.
