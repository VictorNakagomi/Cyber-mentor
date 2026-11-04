# Escada de perguntas — 4 blocos

Perguntas que se complementam: cada bloco só faz sentido depois do anterior. O analista que pula de
OBSERVAR direto pra JULGAR está opinando, não analisando.

**Regra de ritmo:** nunca percorra os 4 blocos no mesmo ritmo. Se ele travar em OBSERVAR, fique em
OBSERVAR. O erro mais comum do mentor é empurrar o analista pra frente pra sessão "render".

---

## Bloco 1 — OBSERVAR
*Separar o que está na tela do que está na cabeça.*

**Ancoragem**
- O que você está vendo? Me descreva sem interpretar nada.
- Qual a diferença entre o que o log diz e o que você concluiu dele?

**Detecção** (por que a regra disparou)
- O que exatamente essa regra testou? Qual a condição dela?
- Qual campo desse evento satisfez a condição?
- Esse é o comportamento que a regra *pretendia* pegar, ou ela pegou outra coisa por tabela?
- Se isso for falso positivo, o problema está no dado, na regra ou no contexto?

**Telemetria** (o que a ferramenta pode provar)
- Que ferramenta geraria o log que provaria isso?
- Essa ferramenta **consegue** ver isso? O que ela não vê?
- Tem algo que essa fonte *parece* provar mas não prova?

→ Detalhe em `logica-deteccao.md` e `telemetria.md`.

---

## Bloco 2 — EXPLICAR
*Mecanismo antes de conclusão.*

- Por que isso funciona tecnicamente? Me explica o passo a passo.
- Qual artefato específico comprova esse passo?
- Se eu tirasse esse artefato da mesa, sua conclusão ainda fica de pé?
- Isso é evidência, inferência ou suposição? *(pergunta de repetição — use sempre)*
- Como você explicaria esse mecanismo pra alguém de fora da área?

---

## Bloco 3 — CORRELACIONAR
*Ligar fontes e montar o tempo.*

**Pivô**
- Qual campo liga esse log ao outro? Host, usuário, IP, hash, sessão?
- Esse pivô é confiável? Dois eventos com o mesmo IP são a mesma coisa?

**Timeline**
- O que veio antes disso? Como entrou?
- O que veio depois? O que ele fez com o que conseguiu?
- Esses dois eventos estão na ordem que o relógio diz, ou na ordem que a causa diz?
- Qual o maior buraco da sua timeline? O que você precisaria pra fechar?

**Macro**
- O que isso diz sobre a campanha? É oportunista ou direcionado?
- Qual o impacto no negócio se sua hipótese estiver certa?
- E se estiver certa pela metade?

→ Detalhe em `correlacao-timeline.md`.

---

## Bloco 4 — JULGAR
*Decidir, e saber o custo de decidir.*

**Criticidade**
- Qual a criticidade real? Me justifica sem usar a severidade do alerta.
- Que fator pesou mais: ativo, estágio, escopo ou confirmação?
- O que faria essa criticidade subir? O que faria descer?

**Contrafactual**
- O que te faria mudar de opinião?
- Qual evidência derrubaria sua hipótese principal de uma vez?

**Ação**
- Qual sua próxima ação, e qual o custo dela? Quem para de trabalhar?
- O que você ganha esperando uma hora? O que você perde?

**Lacuna** *(nunca pule — é o que mais alimenta o baseline)*
- O que você **não** sabe e precisaria saber?
- Se tivesse que passar isso no handoff agora, o que o próximo turno reclamaria?

→ Detalhe em `criticidade.md`.

---

## Perguntas de resgate

Quando ele travar, não responda. Use uma destas:

| Situação | Pergunta |
|---|---|
| travou em branco | "o que você descartaria com certeza? comece pelo que não é" |
| chutando | "qual a sua confiança nisso, de 0 a 4? e por quê não é 4?" |
| preso numa hipótese | "se você fosse provar que está errado, por onde começaria?" |
| pulou pra conclusão | "volta um passo: qual log te deu isso?" |
| usando jargão como muleta | "me explica esse termo sem usar o termo" |
| quer a resposta | "te dou uma dica ou você quer mais 2 minutos?" |

## Encerramento de qualquer sessão

Sempre as mesmas três, nessa ordem:
1. Me resume o caso em 3 frases, como se fosse pro gestor.
2. Qual foi a sua maior incerteza hoje?
3. O que você quer gravar como lacuna pra revisar depois?
