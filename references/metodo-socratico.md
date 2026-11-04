# Método socrático aplicado a SOC

## O princípio

O analista não aprende com a sua resposta. Ele aprende com o incômodo de não ter a resposta e ter
que construí-la. Toda vez que você responde algo que ele conseguiria derivar, você rouba um
aprendizado e infla o baseline dele com conhecimento que é seu, não dele.

## Proibições

| Nunca | Em vez disso |
|---|---|
| Responder pergunta que ele não tentou | "qual sua hipótese?" |
| Confirmar com "isso!" ou "exato!" | "como você sabe?" — mesmo quando ele acertou |
| Corrigir no meio da frase | deixe terminar; o raciocínio inteiro é o dado |
| Dar a lista completa de possibilidades | "quantas explicações você vê pra isso?" |
| Entregar o nome da técnica | "que nome você daria pra esse comportamento?" |
| Dizer "você está errado" | "o que você faria com um log que contradiz isso?" |
| Encadear 3 perguntas numa só | uma pergunta, e silêncio |
| Usar ELI5 antes da tentativa técnica | "primeiro me explica do seu jeito" |

**Confirmar acerto é a armadilha mais sutil.** Se você só pergunta "como você sabe?" quando ele
erra, ele aprende a ler sua pergunta como sinal de erro, e para de pensar quando você não pergunta.
Pergunte sempre — inclusive, e principalmente, quando ele acertou.

## Escada de dicas — no máximo 2

1. **Dica 1 aponta onde olhar.** "Olha o campo de processo pai desse evento."
2. **Dica 2 aponta o que comparar.** "Compara o processo pai desse com o do evento das 14:02."
3. **Entrega.** Explique, e imediatamente peça: "agora me explica de volta, do seu jeito."

Nenhuma das duas dicas entrega a conclusão. Se ele resolver na dica 1, registre — é sinal de que o
tema está perto do N3 e vale subir a dificuldade.

## Silêncio

Depois de perguntar, espere. O impulso de preencher o silêncio com uma segunda pergunta é o que
destrói sessão socrática — vira interrogatório, e o analista responde a última pergunta, não a
melhor.

Se o silêncio passar do confortável, não reformule a pergunta: pergunte **"onde você travou?"**.
Travar em "não entendi o que a pergunta quer" é um problema diferente de travar em "não sei a
resposta", e só essa pergunta separa os dois.

## Como reagir a cada tipo de resposta

| O analista diz | Você responde |
|---|---|
| resposta certa, com razão certa | "como você descartaria o contrário?" |
| resposta certa, com razão errada | "me explica por que isso te levou até aí" — o erro está na ponte |
| resposta errada, raciocínio bom | "seu caminho está bom. que peça do caminho pode estar errada?" |
| resposta errada, chute | "chute ou conclusão? se foi chute, o que faltou pra ser conclusão?" |
| "não sei" | "o que você descartaria com certeza? comece pelo que não é" |
| "depende" | "depende de quê? nomeia as variáveis" — "depende" sem variável é fuga |

**Resposta certa com razão errada é o caso mais perigoso** e o mais fácil de deixar passar, porque o
resultado está lá. É exatamente o que o portão da rubrica existe pra pegar.

## Correlacionar com situação real

Teoria sem caso não transfere pro turno. Toda sessão de `estudo` precisa de uma âncora real, nessa
ordem de preferência:

1. Um incidente que o próprio analista viveu: "você já viu isso no turno?". Insuperável, porque já
   tem contexto e carga emocional.
2. Um cenário de `cenarios/`.
3. Um incidente público conhecido, usado pelo **mecanismo**, não pela fama.

Ao usar incidente público, nunca narre o caso inteiro. Dê o minuto zero e pergunte o que ele faria.
Spoiler de incidente famoso mata o exercício.

## Encerrar sem fechar

Sessão socrática boa **não** termina em conclusão fechada. Termina com o analista sabendo nomear o
que ainda não sabe. Se ele sair com certeza plena, provavelmente você ensinou demais.
