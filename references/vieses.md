# Vieses cognitivos na análise de incidente

Analista não erra por falta de conhecimento com a frequência que erra por viés. Viés é barato de
ensinar e cada um tem um **antídoto operacional** — uma pergunta que o neutraliza na hora.

Use quando o analista travar numa hipótese, quando fechar rápido demais, ou quando a dimensão 3 da
rubrica (hipóteses alternativas) ficar baixa duas avaliações seguidas.

## Fechamento prematuro
A primeira explicação plausível vira a conclusão, e a investigação passa a procurar confirmação.
É o viés nº 1 do SOC, porque a fila pressiona por fechar ticket.

**Sintoma:** o analista descreve o caso no passado ("o usuário clicou no phishing") antes de ter
provado o clique.
**Antídoto:** "me dá a segunda explicação mais provável. Agora me diz o que separa as duas."

## Viés de confirmação
Depois de ter hipótese, ele busca o log que confirma e não busca o que refuta. Pior: encontra, e isso
aumenta a confiança sem aumentar a evidência.

**Sintoma:** todas as consultas dele testam a mesma hipótese por ângulos diferentes.
**Antídoto:** "qual consulta **derrubaria** sua hipótese? roda essa agora."

## Ancoragem
O primeiro número visto domina o julgamento. Em SOC, o âncora é quase sempre **a severidade do
alerta** — e é por isso que ela é regra dura da skill (→ `criticidade.md`).

**Sintoma:** criticidade final igual à severidade da regra, com justificativa construída depois.
**Antídoto:** "julga a criticidade sem olhar a severidade. Agora compara as duas e explica a
diferença."

## Heurística de disponibilidade
O incidente recente ou famoso parece mais provável. Depois de uma semana de ransomware, tudo parece
ransomware.

**Sintoma:** hipótese inicial é exatamente o último caso grave que ele viu.
**Antídoto:** "o que neste caso é **diferente** daquele outro?"

## Viés de automação
Se a ferramenta disse, é verdade. O veredito do EDR, o score do SIEM e a reputação do feed de intel
viram fato sem revisão.

**Sintoma:** "o EDR disse que é limpo" como fim da investigação.
**Antídoto:** "o que a ferramenta precisaria ver pra dizer isso? ela vê?" (→ `telemetria.md`)

## Viés de ausência
Tratar "não achei log" como "não aconteceu". Em nuvem e em host sem agente isso é quase sempre
errado.

**Sintoma:** conclusão negativa apoiada em busca vazia.
**Antídoto:** "isso não existe, ou você não achou? escolhe entre as quatro causas de ausência."

## Excesso de confiança
Confiança declarada acima da acurácia real. É o que a métrica de **calibração** da rubrica mede, e
o risco operacional é fechar incidente cedo.

**Sintoma:** calibração positiva alta por 3+ avaliações.
**Antídoto:** peça a confiança de 0 a 4 **antes** da conclusão, e depois: "o que falta pra ser 4?"

## Custo irrecuperável
Três horas investigando uma hipótese tornam difícil abandoná-la. O investimento vira argumento.

**Sintoma:** ele defende a hipótese citando o esforço gasto.
**Antídoto:** "se você estivesse começando agora, com o que sabe, essa seria sua hipótese?"

## Viés de escopo
Assumir que o escopo encontrado é o escopo real. "Só um host" quase sempre é "só um host que eu
achei".

**Sintoma:** escopo declarado sem dizer como foi delimitado.
**Antídoto:** "como você sabe que não tem um segundo? que busca provaria isso?"

## Como trabalhar na sessão

Não ensine a lista. Viés se aprende **sendo pego em flagrante**.

1. Plante a armadilha. Todo caso em `cenarios/` tem red herring exatamente para isso — é o que torna
   a dimensão 3 da rubrica mensurável.
2. Deixe o analista morder. Não avise.
3. Quando a conclusão estiver declarada, libere a evidência que a derruba.
4. **Não diga qual viés foi.** Pergunte: "o que te levou a aceitar aquilo tão rápido?"
5. Só depois dê o nome. Nome dado antes da experiência é vocabulário; dado depois, é aprendizado.

E o fechamento que vale mais que a aula: **"em que momento exato você podia ter percebido?"**
