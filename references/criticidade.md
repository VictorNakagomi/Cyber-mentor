# Criticidade — julgar a gravidade real

## A regra que o analista mais viola

> **Criticidade não é a severidade do alerta.**

A severidade da regra foi escrita **antes de o incidente existir**, por alguém que não sabia em que
ativo ela ia disparar, com qual usuário, em que horário, nem com que mais aconteceria junto. É uma
opinião genérica. Criticidade é um julgamento situado.

Se o analista disser "é alta porque a regra é alta", isso é um erro a ser trabalhado, não uma
resposta. É a regra dura nº 8 da skill.

Analogia (de `eli5.md`): criticidade não é o quanto o alarme é alto — é o que tem no quarto onde ele
tocou. Alarme alto em quarto vazio é menos grave que alarme baixo no cofre.

## Os seis fatores

Faça o analista pontuar cada um e, no fim, dizer **qual pesou mais**. A nota final importa menos que
saber nomear o fator dominante.

**1. Valor e exposição do ativo**
Não o nome bonito do host: o que ele guarda, a quem serve, e o que ele alcança. Um jump server sem
dado nenhum pode valer mais que um file server, porque alcança tudo.
→ "esse host guarda o quê, serve a quem, e alcança o quê?"

**2. Estágio na kill chain**
Reconhecimento e acesso inicial são reversíveis e baratos. Movimentação lateral, escalada e
exfiltração não são. Mesmo ativo, estágio diferente, criticidade diferente.
→ "o atacante já conseguiu o que queria, ou ainda está tentando?"

**3. Escopo**
Um host, um usuário, um segmento, ou o domínio. Escopo é o fator que mais muda a criticidade **para
cima** durante a investigação, e por isso criticidade deve ser revisada, não definida uma vez.
→ "quantas entidades estão envolvidas, e como você sabe que não são mais?"

**4. Confirmação (confiança)**
O comportamento está provado, inferido ou suposto? Vem de quantas fontes independentes? Informado
pela lógica da regra (→ `logica-deteccao.md`).
→ "qual sua confiança de 0 a 4, e o que falta pra ser 4?"

**5. Reversibilidade**
O que já não pode ser desfeito. Dado exfiltrado não volta. Credencial vazada só se rotaciona.
Ransomware cifrado é irreversível sem backup. Processo malicioso ainda rodando é reversível **agora**.
→ "o que ainda dá pra impedir, e o que já era?"

**6. Urgência — o teste de uma hora**
Diferente de impacto, e é o fator que mais se confunde. Pergunta única:
→ **"o que muda se você esperar uma hora?"**
Se nada muda, não é urgente — pode ser gravíssimo, mas não urgente. Se em uma hora o atacante
provavelmente terá o domínio, é urgente mesmo com impacto atual baixo.

## Fórmula orientadora

```
Prioridade  =  Impacto  ×  Confiança  ×  Urgência

Impacto    = valor do ativo + estágio + escopo + reversibilidade
Confiança  = quantas fontes independentes, e quão determinística a detecção
Urgência   = o que se perde esperando uma hora
```

Multiplicação, não soma: **confiança baixa derruba a prioridade mesmo com impacto alto**. É assim
que se evita o SOC que escala tudo. E o inverso — confiança alta com impacto baixo também não sobe.

## Matriz de decisão

| Prioridade | Descritor | Exemplo |
|---|---|---|
| **P1** | impacto alto, confiança alta, irreversível em curso | ransomware cifrando compartilhamento agora; DA comprometido confirmado |
| **P2** | impacto alto, confiança média, ou impacto médio com urgência | lateral confirmada em um host, escopo ainda indefinido |
| **P3** | confiança alta, impacto contido e reversível | malware commodity bloqueado pelo EDR, host único, sem lateral |
| **P4** | baixa confiança ou comportamento legítimo provável (TPB) | desvio de volume de upload num host de backup em janela de manutenção |

## Os cinco erros de julgamento

Trabalhe cada um explicitamente — eles aparecem toda semana:

1. **Herdar a severidade do alerta.** Ancoragem pura. A regra não conhecia o contexto.
2. **Inflar pelo nome do host.** `SRV-DC-PROD-01` não é crítico porque o nome é assustador: é
   crítico pelo que faz. E `WKS-0455` pode ser a estação do CFO.
3. **Deflacionar por escopo aparente.** "Só um host" quase sempre significa "só um host **que eu
   achei**". Escopo não confirmado não é escopo pequeno.
4. **Confundir urgência com impacto.** Backup antigo exfiltrado tem impacto alto e urgência baixa.
   Credencial de serviço vazada há 10 minutos tem o oposto. Tratar os dois igual erra os dois.
5. **Travar a criticidade no primeiro julgamento.** Criticidade é revisada a cada evidência nova.
   Analista que não revisa está defendendo o julgamento inicial, não investigando.

## O contrafactual de criticidade

Nunca aceite nota sem estas duas respostas — elas são a própria dimensão 3 da rubrica, aplicada a
julgamento:

- **"O que faria essa criticidade subir?"** → se ele não souber, não entendeu o que está em jogo.
- **"O que faria descer?"** → se ele não souber, está defendendo a nota, não analisando.

Analista N4 responde as duas sem hesitar e já sabe qual consulta responderia cada uma.

## Comunicar criticidade

Reportar criticidade para gestão em três frases, nesta ordem (vira exercício do eixo `comunicacao`):

1. **O que aconteceu**, sem jargão e sem nome de ferramenta.
2. **O que isso permite ao atacante** — impacto em termos de negócio, não de técnica.
3. **O que preciso agora**, e o custo de não fazer.

Exemplo: *"Uma estação do financeiro executou um programa que estabeleceu canal de comando externo.
Com esse canal, o atacante consegue tentar alcançar os servidores de pagamento. Preciso isolar a
estação agora — a pessoa para de trabalhar por cerca de 1 hora, e sem isso não consigo garantir que
o acesso não se espalhe."*

O que **não** entra: nome da regra, score, hash, porta. Nada disso ajuda a decidir.

## Exercícios

1. Mesmo alerta de PowerShell codificado, três contextos: estação de estagiário, notebook do CFO,
   jump server de TI. Classifique os três e diga qual fator mudou.
2. "Exfiltração confirmada de um banco de dados — de backup de 2019, desativado." Impacto? Urgência?
   São iguais?
3. "Confiança 1 de 4, impacto potencial máximo." O que você faz, e como justifica não escalar como
   P1?
4. Você classificou P3. Uma hora depois aparece o segundo host. Que fator mudou, e para quanto vai?
5. Explique para um gerente não técnico, em três frases, por que um alerta "baixo" do SIEM virou P1.
