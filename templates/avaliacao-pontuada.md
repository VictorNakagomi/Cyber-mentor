---
analista: <nome>
tema: <tema>
eixo: <eixo>
data: <AAAA-MM-DD>
origem: <colado|whisper|telegram|whatsapp>
confianca_declarada: <0-4>
portao: <aprovado|fechado>
portao_motivo: <vazio se aprovado; se fechado, o erro factual que invalidou a conclusão>
rigor_epistemico: <0-4>
arquitetura: <0-4>
alcance: <micro|micro-macro|macro-solto>
hipoteses_alternativas: <0-4|na>
comunicacao: <0-4>
total: <0-16>
nivel_apurado: <1-5>
---

# Avaliação — <tema>

## Portão: <aprovado|fechado>

<Se fechado: qual erro factual invalidou a conclusão, com trecho literal. A avaliação NÃO CONTA —
não pontua, não sobe nível, não desce nível. Registrar lacuna e pedir nova gravação.>

## Dimensão 1 — Rigor epistêmico: <n>/4

> "<trecho literal da transcrição que justifica a nota>"

<Uma frase de devolutiva, dirigida ao processo. "Você afirmou X como fato sendo inferência", não
"faltou rigor".>

## Dimensão 2 — Arquitetura do raciocínio: <n>/4  `[<alcance>]`

> "<trecho literal>"

<Uma frase. Se o alcance ficou em `micro`, nomeie até onde ele chegou e qual elo faltava para subir.>

## Dimensão 3 — Hipóteses alternativas: <n>/4

> "<trecho literal>"

<Uma frase. Se o caso não tinha armadilha, marque `na` e não pontue esta dimensão.>

## Dimensão 4 — Comunicação (ELI5): <n>/4

> "<trecho literal>"

<Uma frase. Avalie: analogia própria ou emprestada? o mecanismo sobreviveu? nomeou onde quebra?>

## Total e nível

```
Total: <n>/16        →  N<n> <nome do nível>
Confiança declarada: <n>/4
Calibração: <confianca_declarada - total/4>   <leitura: calibrado | excesso | subconfiança>
```

<Nível só sobe com 2 avaliações consecutivas nessa faixa. Diga explicitamente se esta é a primeira
ou a segunda.>

## Próximo passo

<UM único. Não cinco.>
