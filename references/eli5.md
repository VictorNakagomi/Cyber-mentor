# ELI5 — explicar como se fosse criança

## Dois papéis, não um

ELI5 tem aqui **duas funções opostas**, e confundi-las quebra a skill:

1. **Ferramenta de ensino** — você explica pro analista, depois que ele tentou.
2. **Instrumento de avaliação** — ele explica pra você, e isso é a prova (dimensão 4 da rubrica).

A função 2 é a razão de a skill existir. Quem não consegue explicar em linguagem de criança não
entendeu. É a técnica de Feynman, e é o teto da matriz de competências (N5 Ensina).

## Regra de ordem

**Nunca dê ELI5 antes de o analista tentar a versão técnica.** O ELI5 é ponte depois da tentativa,
nunca atalho antes dela. Se ele pedir "explica simples" de cara, devolva: "me explica primeiro do
seu jeito, mesmo errado — depois eu simplifico e a gente compara".

## Como construir um ELI5 que não mente

Analogia é modelo, e todo modelo é errado em algum ponto. ELI5 honesto tem 4 partes:

1. **A cena** — algo do mundo físico que a criança conhece.
2. **O mapeamento** — quem é quem: "o porteiro é o firewall".
3. **O mecanismo** — o que acontece na cena, na mesma ordem em que acontece na realidade.
4. **Onde a analogia quebra** — o ponto em que a cena deixa de valer.

A parte 4 é obrigatória, e é o que separa ELI5 de simplificação errada. Também é o que, na
avaliação, separa nota 3 de nota 4: **só sabe onde a analogia falha quem entende o mecanismo por
baixo dela.**

## Biblioteca de analogias

Ponto de partida, não script. Analogia criada pelo próprio analista vale mais que a sua.

| Conceito | Cena | Onde quebra |
|---|---|---|
| Firewall | porteiro que só olha a lista de quem pode entrar e por qual portão | não abre a mochila de quem entrou; confere nome e porta, nada mais |
| Proxy | recepcionista que busca as coisas pra você e anota o endereço | com TLS ele vê o endereço, não o conteúdo |
| DNS | agenda de telefone: você sabe o nome, ela dá o número | a agenda também serve pra mandar recado escondido (tunelamento) |
| DNS tunneling | mandar uma carta picada dentro de vários pedidos de telefone | pedir telefone é normal; pedir 4 mil vezes em 10 minutos não é |
| EDR | câmera dentro da casa, que filma quem abriu qual porta | não filma a rua; perde tudo que acontece fora do host |
| SIEM | mesa onde se juntam as fotos de todas as câmeras pra montar a história | só tem as fotos que alguém mandou pra mesa: o que não foi coletado não existe |
| Kerberos / TGT | pulseira de parque: mostra uma vez na entrada e usa em todos os brinquedos | quem toma a máquina que fabrica pulseira entra em tudo |
| Golden Ticket | roubar a máquina que **fabrica** a pulseira, não uma pulseira | trocar sua pulseira não resolve: tem que trocar a máquina (`krbtgt`) |
| Hash de senha | impressão digital da senha, não a senha | em alguns protocolos a digital já basta pra entrar (pass-the-hash) |
| Beaconing | criança que liga pra casa a cada 5 minutos pedindo instrução | pessoa liga em hora irregular; programa liga com régua, e o padrão denuncia |
| Exfiltração | tirar foto do caderno e mandar aos poucos pra ninguém notar a falta | o caderno continua lá; nada "sumiu", e é por isso que passa batido |
| Persistência | deixar a janela destrancada pra voltar depois | não é o ataque: é o seguro do atacante contra você reiniciar a máquina |
| LOLBin | usar a chave de fenda da própria casa pra arrombar o armário da casa | a ferramenta é legítima; o estranho é quem pegou e pra quê |
| Lateral movement | andar de sala em sala com o crachá de outra pessoa | cada porta aberta parece normal; o padrão de salas é que não é |
| Privilege escalation | criança que acha o chaveiro mestre do zelador | depois disso não precisa arrombar mais nada |
| Falso positivo | alarme que toca quando o gato passa | o alarme funcionou: ele só não sabe diferenciar gato de ladrão |
| TP benigno | o alarme toca, **era** uma pessoa, e a pessoa mora ali | o comportamento aconteceu de verdade, e é autorizado |
| Threshold de regra | "me avisa se bater mais de 10 vezes" | em 9 vezes o alarme fica quieto, e quem sabe disso bate 9 |
| Criticidade | não é o quanto o alarme é alto: é o que tem no quarto onde ele tocou | alarme alto em quarto vazio é menos grave que alarme baixo no cofre |
| Kill chain | roteiro de assalto: olhar a casa, entrar, achar o cofre, levar | a ordem se repete e volta atrás; não é fila |
| IOC vs. TTP | IOC é o rosto do ladrão; TTP é o jeito dele arrombar | rosto se troca com cirurgia; jeito de arrombar, não |

## Avaliando o ELI5 do analista

Quando ele explica, escute procurando:

- **Analogia emprestada ou própria?** Reproduzir a sua analogia é N2. Criar uma que funciona é N4+.
- **O mecanismo sobreviveu à simplificação?** Simplificar errado é perder a ordem causal — não é
  perder termo técnico.
- **Ele nomeou onde quebra?** Sem isso, o teto é nota 3.
- **Usou jargão escondido?** "Daemon", "handshake", "payload", "hash" não são linguagem de criança.

Pergunta de teste quando a explicação parece boa demais: **"e por que não funciona assim do outro
lado?"** Analogia decorada não aguenta essa pergunta.
