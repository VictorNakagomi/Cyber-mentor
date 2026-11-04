# Protocolo de criação de casos

## A regra que decide banco ou on-demand

Ela sai direto da decisão de desenho "**só áudio avaliado move nível**":

| Para | Fonte do caso | Por quê |
|---|---|---|
| **Avaliação** (move nível) | **sempre do banco** | nível tem que ser comparável entre pessoas |
| **Treino / estudo** (não pontua) | **on-demand** | mira a lacuna específica daquele analista hoje |

**Por que avaliação não pode usar caso gerado na hora.** Se cada analista enfrenta um caso diferente,
dois "N3 em `telemetria`" não significam a mesma coisa: dificuldades diferentes, armadilhas de
qualidade diferente, nenhum gabarito revisado. Baseline que não é comparável entre pessoas não
serve para decidir plano de treino, alocação de turno ou promoção — que é o motivo de o baseline
existir.

**Por que treino é melhor on-demand.** Nada é pontuado, então não precisa de gabarito validado. E
on-demand tem uma vantagem que o banco nunca terá: você gera mirando a lacuna aberta. Para um
analista que inverte direção de tráfego, dá para fabricar um caso curto que force leitura de
direção três vezes em contextos diferentes — coisa que nenhum banco teria pronto.

## Promoção: o banco cresce do uso

Caso on-demand que funcionou bem **não se joga fora: promove-se**. Banco construído em lote fica
genérico; banco construído do que realmente pegou os analistas fica afiado.

Para promover, o caso precisa ganhar o que lhe faltava:

- [ ] `gabarito-raciocinio.md` escrito — o **caminho**, não a resposta
- [ ] armadilha plantada e documentada nas notas de mentor
- [ ] `evidencias/_indisponivel.md` com a cegueira proposital
- [ ] técnicas ATT&CK mapeadas no frontmatter
- [ ] nível alvo declarado
- [ ] entrada no `indice.md` (criar o índice a partir de ~6 casos)

Critério para promover: **pegou pelo menos um analista** num ponto que valia aprender. Caso que
todo mundo resolve direto não entra no banco — não discrimina nada.

## Regras não negociáveis (banco e on-demand)

Valem para qualquer caso, inclusive o gerado em 30 segundos no meio de uma sessão.

### 1. Minuto zero sem adjetivo, sem veredito, sem narrativa
Entregue o que o SOC veria no instante do alerta e nada mais. Se o bloco inicial dá a resposta, o
caso está mal escrito. Proibido: "suspeito", "malicioso", "comprometido", "o atacante".

### 2. Armadilha obrigatória
Sem *red herring* plausível, a **dimensão 3 da rubrica** (hipóteses alternativas) não é mensurável —
o analista acerta por sorte e você pontua errado. Se o caso não tem armadilha, marque
`armadilha: nao` no frontmatter e **não pontue** aquela dimensão.

A armadilha boa tem duas propriedades:
- **é plausível o suficiente para ser aceita** por um analista competente com pressa
- **tem mais de um caminho de desmonte** — no caso 001, horário **e** exclusão da regra. Um caminho
  só transforma o exercício em sorte

### 3. Pelo menos uma fonte ausente de propósito
Toda telemetria real tem buraco. O caso precisa de uma pergunta que o analista vai querer fazer e
para a qual **nenhuma fonte do ambiente responde**. Documente em `evidencias/_indisponivel.md`,
classificando a causa: não coletado, não parseado, fora da retenção, filtrado.

Quando ele pedir a fonte ausente, **nunca diga "não existe"**. Pergunte "que ferramenta geraria esse
log?" e "ela está no escopo?" antes de mostrar.

### 4. Evidência liberada sob hipótese
Nunca entregue `evidencias/` em lote. Uma por vez, e só quando o analista pedir **aquela** fonte
**e** disser que hipótese ela testa. Pedido sem hipótese volta com "o que você espera encontrar aí?"

### 5. Multi-ferramenta, com pelo menos um pivô fraco
O caso precisa de no mínimo três fontes, e de pelo menos uma oportunidade de pivotar errado: IP
interno sem janela de tempo, IP externo de CDN compartilhado, ou correlação só por timestamp.

### 6. Fuso misturado em pelo menos um log
Pelo menos uma fonte em fuso diferente das outras, com o nome da coluna dizendo (`eventtime_utc`).
Timeline que não exige conversão não treina timeline.

> **Cuidado:** não escreva aviso editorial do tipo "ATENÇÃO: este log está em UTC" no corpo do log.
> O nome da coluna é dado; o aviso é você gritando, e desarma a armadilha. Avisos vão nas notas de
> mentor, no fim do arquivo, marcados como não entregar.

### 7. A regra que disparou vem junto, com os sete componentes
`regra.md` é obrigatório, com fonte, observável, condição, threshold, janela, baseline e exclusão.
Sem isso o analista não pode trabalhar o eixo `logica-deteccao`, e a regra é frequentemente a chave
para desmontar a armadilha.

**Plante uma falha real na regra** — regex larga, exclusão explorável, threshold que convida a
fracionar. É o que permite a pergunta "como você passaria por essa regra?"

### 8. Notas de mentor separadas e marcadas
Toda nota para o mentor vai no fim do arquivo, marcada `NÃO ENTREGAR`. Em JSON, use uma chave
`_nota_mentor`. Nunca misture no corpo do que o analista lê.

### 9. Gabarito descreve caminho, não resposta
`gabarito-raciocinio.md` precisa ter: o que é evidência / inferência / suposição, a timeline
esperada com as lacunas como linha, os erros a pegar, a criticidade com o fator dominante nomeado,
e o checklist de lacunas para marcar. Compare o **caminho** do analista, nunca a conclusão.

### 10. Dado sintético, sempre
Nunca use IOC, host, usuário ou IP de incidente real, mesmo "sanitizado". Domínios de exemplo,
RFC 1918 para interno, nomes fictícios.

## Estrutura de arquivos

```
cenarios/<NNN-slug>/
  caso.md                  minuto zero, contexto, escopo de telemetria, entregáveis
  regra.md                 a lógica da detecção + perguntas sobre ela
  evidencias/
    01-..., 02-...         numeradas na ordem provável de pedido
    _indisponivel.md       a cegueira proposital
  gabarito-raciocinio.md   o caminho esperado
```

Use `templates/caso.md` como ponto de partida.

## Receita para gerar on-demand numa sessão

Quando a lacuna é conhecida, 5 passos:

1. **Escolha a lacuna alvo.** Uma, não três. Leia `lacunas.md` do analista.
2. **Escolha o mecanismo** que força aquela lacuna. Lacuna de direção de tráfego → caso com volume
   em duas direções em três fontes. Lacuna de criticidade herdada → alerta `Low` em ativo crítico.
3. **Escreva o minuto zero** em 5 linhas, sem adjetivo.
4. **Fabrique 3 a 4 evidências**, com um pivô fraco e um fuso diferente.
5. **Decida a armadilha** antes de conduzir, e com dois caminhos de desmonte.

Não escreva gabarito para caso on-demand. Se ele funcionar, promova depois — e aí escreva.

## Calibração de dificuldade

| Nível alvo | O caso exige |
|---|---|
| **N2** | ler um log e descrever o que vê, sem correlacionar |
| **N3** | correlacionar duas fontes, classificar TP/TPB/FP, ler a lógica da regra |
| **N4** | questionar o pivô, questionar o baseline da regra, nomear a cegueira, julgar criticidade contra a severidade |
| **N5** | explicar tudo isso para quem não é da área, e dizer onde a própria analogia quebra |

Um caso N4 que o analista N2 resolve está mal calibrado. Um caso N3 que ninguém resolve tem
armadilha sem caminho de desmonte — conserte a armadilha, não o nível.
