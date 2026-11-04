# Rubrica de raciocínio

Avalia **como o analista pensa**, não quanto ele decorou. Aplicada **somente** no modo `avaliar`,
sobre áudio de 5–8 minutos com tema fechado. Sessão diária não usa esta rubrica.

## Por que um portão e não seis notas

Em cibersegurança, um raciocínio **errado, confiante, bem estruturado e bem comunicado** é mais
perigoso que um certo e hesitante. Se correção técnica fosse uma das notas, o erro factual seria
diluído pela média e o analista subiria de nível explicando algo errado com elegância.

Por isso correção técnica é **portão binário**, não dimensão.

## Portão: correção técnica

> Existe erro factual que **invalida a conclusão**?

- **Não** → avaliação prossegue e pontua.
- **Sim** → avaliação **NÃO CONTA**. Não é nota zero. Não pontua, não sobe nível, não desce nível.
  Registra a lacuna em `lacunas.md`, devolve o tema pro estudo e pede nova gravação.

Erro factual periférico que não muda a conclusão **não** fecha o portão — anota em observação e
segue. Exemplo: errar o número da porta do Kerberos num raciocínio correto sobre Golden Ticket não
fecha o portão. Dizer que Golden Ticket é forjado com a hash da conta do usuário (e não da `krbtgt`)
fecha, porque destrói a conclusão sobre contenção.

## As 4 dimensões

Cada uma de 0 a 4. Total 0–16.

### 1. Rigor epistêmico
Separa o que sabe do que acha.

```
0  afirma tudo como fato, sem distinção
1  distingue só quando provocado pelo mentor
2  distingue espontaneamente em parte do raciocínio
3  rotula consistentemente evidência vs. inferência vs. suposição
4  rotula E declara qual evidência mudaria a conclusão
```

### 2. Arquitetura do raciocínio
A cadeia se sustenta, e até onde ela alcança.

```
0  afirmações soltas, sem relação causal
1  cadeia com salto lógico que ele não percebe
2  cadeia válida mas rasa, ou com elo não comprovado
3  cadeia válida, cada elo apoiado em artefato
4  cadeia válida, apoiada, e com os elos frágeis identificados por ele mesmo
```

**Marque também o alcance** — isto não altera a nota, é diagnóstico:
- `[micro]` ficou no artefato/host. Perfil mais comum de L2/L3.
- `[micro→macro]` subiu do artefato até campanha ou impacto de negócio.
- `[macro solto]` falou de impacto sem ancorar em artefato. Pior que `[micro]`.

### 3. Hipóteses alternativas
Considerou outras explicações, ou travou na primeira.

```
0  hipótese única, tratada como certeza
1  reconhece que pode haver outra, sem nomear
2  nomeia uma alternativa mas não a testa
3  nomeia e descarta com evidência
4  nomeia, descarta com evidência, e diz o que faltou para descartar de vez
```

Esta dimensão só é mensurável se o caso tiver **armadilha plantada**. Caso sem red herring não
avalia esta dimensão — marque `n/a` e não divida por ela.

### 4. Comunicação (ELI5)
A criança entenderia.

```
0  só jargão; incompreensível fora da área
1  traduz termos mas perde a lógica no caminho
2  explicação compreensível, com analogia frouxa ou errada
3  analogia correta que sustenta o mecanismo
4  analogia correta E ele aponta onde a analogia quebra
```

O nível 4 aqui é o teste real de domínio: só sabe onde a analogia falha quem entende o mecanismo
por baixo dela.

## Calibração (métrica silenciosa)

O analista declara `confianca_declarada` (0–4) **antes** de receber a nota. Registre:

```
calibracao = confianca_declarada - (total / 4)
```

- Positivo alto e recorrente → excesso de confiança. O risco operacional aqui é fechar incidente
  cedo. Trabalhe `references/vieses.md`.
- Negativo alto e recorrente → subconfiança. O risco é escalar o que daria conta, e não assumir
  conclusão. Trabalhe exposição, não conteúdo.

Calibração **não entra na nota**. É tendência, lida ao longo de 3+ avaliações.

## Progressão de nível

Cada avaliação pontua **um eixo principal** (o tema do áudio). Faixas:

```
≤5      → N1 Reconhece
6–8     → N2 Descreve
9–11    → N3 Aplica
12–14   → N4 Correlaciona
15–16   → N5 Ensina   (exige Comunicação = 4)
```

Duas regras que protegem a credibilidade do baseline:

1. **Nível sobe só com 2 avaliações consecutivas na faixa.** Um áudio bom não faz nível.
2. **Nível nunca desce por avaliação ruim — mas expira.** Eixo sem avaliação há 90 dias vira
   `não verificado`, não rebaixado. Cria pressão de revisão sem punir quem estava certo antes.

Avaliação que fecha o portão não conta para nenhuma das duas regras.

## Como escrever a avaliação

Grave em `dados-analistas/<nome>/avaliacoes/pontuadas/` usando
`templates/avaliacao-pontuada.md`. Regras de redação:

- **Cite a transcrição.** Toda nota precisa de trecho literal que a justifique. Sem citação, a nota
  é opinião e o baseline vira ruído.
- **Uma frase de devolutiva por dimensão**, dirigida ao processo: "você afirmou X como fato sendo
  inferência" e não "faltou rigor".
- **Um único próximo passo.** Não cinco.
