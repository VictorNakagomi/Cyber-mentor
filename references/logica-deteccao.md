# Lógica de detecção — por que a regra disparou

O analista que não sabe por que a regra disparou está julgando o alerta pela cor dele. Este eixo é o
que transforma operador de fila em analista.

## Anatomia de uma regra

Toda detecção, em qualquer produto, tem as mesmas sete partes. Faça o analista preencher as sete
antes de opinar sobre o alerta:

| Parte | Pergunta |
|---|---|
| **Fonte** | que telemetria ela consome? (→ `telemetria.md`) |
| **Observável** | que campo ela olha? |
| **Condição** | que comparação ela faz? igualdade, regex, lista, desvio? |
| **Threshold** | a partir de quanto dispara? |
| **Janela** | em quanto tempo? |
| **Baseline** | comparado com o quê — o próprio usuário, o grupo dele, ninguém? |
| **Exclusão** | o que está em allowlist? |

As duas que ninguém olha são **janela** e **exclusão**, e são as duas que explicam a maioria dos
alertas estranhos.

## As 4 perguntas obrigatórias

Sempre nessa ordem, antes de qualquer conclusão sobre o alerta:

1. **O que exatamente essa regra testou?** (a condição, em português)
2. **Qual campo deste evento satisfez a condição?** (o valor concreto, não a descrição)
3. **Este é o comportamento que a regra pretendia pegar, ou ela pegou outra coisa por tabela?**
4. **Se for falso positivo, o problema está no dado, na regra ou no contexto?**

A pergunta 3 é a que separa N3 de N4: exige entender a **intenção** da detecção, não só a mecânica.

## A classificação em três, não em duas

Verdadeiro positivo / falso positivo é uma dicotomia pobre e produz tuning errado. Use três:

| Classe | O comportamento aconteceu? | É malicioso ou não autorizado? | Ação |
|---|---|---|---|
| **TP — verdadeiro positivo** | sim | sim | resposta a incidente |
| **TPB — verdadeiro positivo benigno** | **sim** | não, é legítimo | exclusão de contexto, **não** mexer na lógica |
| **FP — falso positivo** | **não** | — | corrigir dado, parser, regra ou threshold |

**O TPB é a classe que falta no vocabulário da maioria dos SOCs.** O admin que realmente rodou
`psexec` gerou um evento verdadeiro: a regra funcionou perfeitamente. Classificar isso como falso
positivo leva a mexer na lógica da regra e abrir cegueira real. O que estava faltando era contexto,
não precisão.

Pergunta de mentor: **"o comportamento aconteceu de verdade? se sim, não é falso positivo —
é alguém autorizado fazendo algo que parece ataque. Como você provaria a autorização?"**

## Falso positivo: dado, regra ou contexto

Quando é FP de verdade, a causa define a ação:

**Dado** — o evento está errado ou malformado.
- parser mapeou campo errado (um `destinationaddress` que na verdade é o de origem)
- campo vazio tratado como match
- log duplicado inflando contagem até o threshold
- → verificar o `rawevent` antes de culpar a regra

**Regra** — a lógica não expressa a intenção.
- regex larga demais
- threshold mal calibrado para o volume real
- janela curta ou longa demais
- baseline contaminado: foi aprendido durante um período anormal, então o anormal virou normal
- → tuning de lógica

**Contexto** — a lógica está certa, falta informação do ambiente.
- conta de serviço se comportando como conta de serviço
- scanner de vulnerabilidade autorizado parecendo varredura
- janela de manutenção, migração, teste de pentest contratado
- → enriquecimento ou exclusão, nunca mexer na lógica

## Securonix: o vocabulário

Alinhe o analista no vocabulário real do produto. Confirme os detalhes no seu tenant — políticas e
threat models são customizados por ambiente.

| Conceito | O que o analista precisa entender |
|---|---|
| **Policy** | a regra. Pode ser baseada em regra determinística ou em comportamento/desvio |
| **Violation** | a instância: esta entidade violou esta policy neste momento |
| **Entity (EEO)** | sobre **quem** a violação é — usuário, host, IP, recurso. Policy comportamental sem entidade correta não tem baseline válido |
| **Risk score** | acumula violações ao longo do tempo. Score alto pode ser muitas violações pequenas, não uma grande |
| **Threat model** | encadeia violações em estágios. O alerta de threat model significa **sequência**, não evento |
| **`rg_functionality`** | que tipo de olho gerou o dado. Primeira pergunta de qualquer investigação |

Duas consequências que o analista precisa saber ler:

1. **Score alto ≠ incidente grave.** Score é acumulação. Um usuário com 20 violações de baixa
   relevância pode ter score maior que um com uma violação crítica. Pergunta: "esse score veio de
   uma coisa grave ou de muitas coisas pequenas?"
2. **Policy comportamental só vale se o baseline valer.** Usuário novo, mudança de função, retorno de
   férias ou migração contaminam baseline. Pergunta: "quanto tempo de histórico essa entidade tem?"

## O que a regra NÃO pegaria

A pergunta mais avançada deste eixo, e a que mais ensina:

> **"Como você passaria por essa regra sem ela disparar?"**

Força o analista a ler a detecção como atacante, e expõe automaticamente threshold, janela e
exclusão. Exemplos do raciocínio que ela produz:

- threshold de 10 em 5 minutos → fazer 9 em 5 minutos, indefinidamente
- regra que olha `powershell.exe` por nome → renomear o binário, ou usar outro host de runtime
- regra que depende de agente EDR → operar no host sem agente
- regra que olha porta 445 → usar outro transporte
- regra com exclusão para contas de serviço → se passar por conta de serviço

Toda detecção tem evasão. O analista que acha que não tem ainda não entendeu a regra.

## Conectando com criticidade

A severidade da regra é uma opinião **escrita antes de o incidente existir**, por alguém que não
sabia em que ativo ela ia disparar. Por isso não se herda criticidade de severidade — ver
`criticidade.md`.

Mas a lógica da regra **informa confiança**, e confiança é fator de criticidade:
- regra determinística com condição precisa → confiança alta
- regra comportamental com baseline curto → confiança baixa
- threat model com 3 estágios casados → confiança alta, porque exige coincidência improvável

## Exercícios

1. "Regra: mais de 50 negações de autenticação para a mesma conta em 10 minutos. O que ela
   pretendia pegar? Dê dois ataques que ela pega e dois que ela não pega."
2. "O alerta disparou por desvio de volume de upload. Que três coisas legítimas produzem esse
   desvio? Como você separa uma da outra?"
3. "Score do usuário subiu 400 pontos em 2 dias sem nenhuma violação crítica. O que você investiga
   primeiro?"
4. "A regra tem exclusão para `svc_backup`. Como você verificaria se um atacante está usando isso?"
5. "Classifique como TP, TPB ou FP e justifique: PowerShell com `-enc` rodando num host de TI às
   3h da manhã, no mesmo horário em que a janela de manutenção está aberta no ITSM."
