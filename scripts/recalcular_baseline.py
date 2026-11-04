#!/usr/bin/env python3
"""Recalcula o baseline de um analista a partir das avaliacoes pontuadas.

O baseline NUNCA e escrito a mao: ele e derivado das avaliacoes, para ser auditavel.
Toda nota rastreia para um arquivo em avaliacoes/pontuadas/.

Uso:
    python recalcular_baseline.py <nome>          # um analista
    python recalcular_baseline.py --time          # consolidado do time

A pasta de dados e resolvida nesta ordem:
    1. variavel de ambiente CYBER_MENTOR_DADOS
    2. <diretorio atual>/dados-analistas, se existir
    3. <pasta do nucleo>/../dados-analistas

Stdlib apenas. Sem dependencias.
"""

import json
import os
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

EXPIRA_DIAS = 90


def resolver_raiz():
    """Resolve a pasta de dados do analista. Ver docstring do modulo."""
    env = os.environ.get("CYBER_MENTOR_DADOS")
    if env:
        return Path(env).expanduser().resolve()

    no_cwd = Path.cwd() / "dados-analistas"
    if no_cwd.is_dir():
        return no_cwd.resolve()

    # Path.resolve() segue junction no Windows, entao isto aponta para o nucleo
    # real mesmo quando o script roda via ~/.claude/skills/cyber-mentor.
    relativo = (Path(__file__).resolve().parent.parent.parent / "dados-analistas").resolve()

    # Guarda: dado de analista nunca mora dentro da arvore de skills.
    if ".claude" in relativo.parts:
        sys.exit(
            "erro: o caminho de dados caiu dentro de .claude "
            f"({relativo}).\n"
            "Defina CYBER_MENTOR_DADOS apontando para a pasta de dados, ou rode o "
            "script a partir da pasta que contem dados-analistas."
        )
    return relativo


RAIZ = resolver_raiz()

NIVEIS = {1: "Reconhece", 2: "Descreve", 3: "Aplica", 4: "Correlaciona", 5: "Ensina"}

EIXOS = {
    "A - Fundamentos tecnicos": ["redes", "endpoint", "identidade", "cloud", "malware"],
    "B - Pratica analitica": ["telemetria", "correlacao-timeline", "logica-deteccao",
                              "criticidade", "siem-query"],
    "C - Processo e oficio": ["processo-ir", "threat-intel", "comunicacao"],
}
TODOS_EIXOS = [e for grupo in EIXOS.values() for e in grupo]


def ler_frontmatter(caminho):
    """Parser minimo de frontmatter YAML chave: valor."""
    texto = caminho.read_text(encoding="utf-8")
    if not texto.startswith("---"):
        return None
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return None
    dados = {}
    for linha in partes[1].splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or ":" not in linha:
            continue
        chave, _, valor = linha.partition(":")
        dados[chave.strip()] = valor.strip().strip('"').strip("'")
    return dados


def num(valor, default=None):
    try:
        return int(str(valor).strip())
    except (TypeError, ValueError):
        return default


def calcular_total(fm):
    """Total 0-16. Se hipoteses_alternativas = na, normaliza as 3 restantes."""
    rigor = num(fm.get("rigor_epistemico"))
    arq = num(fm.get("arquitetura"))
    com = num(fm.get("comunicacao"))
    hip_raw = str(fm.get("hipoteses_alternativas", "")).strip().lower()

    if None in (rigor, arq, com):
        return None, None

    if hip_raw in ("na", "n/a", ""):
        return round((rigor + arq + com) * 4 / 3), com
    hip = num(hip_raw)
    if hip is None:
        return None, None
    return rigor + arq + com + hip, com


def faixa(total, comunicacao):
    """Total 0-16 -> nivel 1-5. N5 exige comunicacao = 4."""
    if total <= 5:
        return 1
    if total <= 8:
        return 2
    if total <= 11:
        return 3
    if total <= 14:
        return 4
    return 5 if comunicacao == 4 else 4


def carregar_avaliacoes(pasta):
    """Le as pontuadas e devolve dict eixo -> lista ordenada por data."""
    por_eixo = {}
    descartadas = 0
    portao_fechado = 0

    diretorio = pasta / "avaliacoes" / "pontuadas"
    if not diretorio.is_dir():
        return por_eixo, 0, 0

    for arquivo in sorted(diretorio.glob("*.md")):
        fm = ler_frontmatter(arquivo)
        if not fm:
            descartadas += 1
            continue

        eixo = fm.get("eixo", "").strip()
        if eixo not in TODOS_EIXOS:
            print(f"  aviso: eixo desconhecido '{eixo}' em {arquivo.name}")
            descartadas += 1
            continue

        if fm.get("portao", "").strip().lower() == "fechado":
            portao_fechado += 1
            continue

        total, com = calcular_total(fm)
        if total is None:
            print(f"  aviso: dimensoes incompletas em {arquivo.name}")
            descartadas += 1
            continue

        try:
            quando = datetime.strptime(fm.get("data", ""), "%Y-%m-%d").date()
        except ValueError:
            print(f"  aviso: data invalida em {arquivo.name}")
            descartadas += 1
            continue

        por_eixo.setdefault(eixo, []).append({
            "arquivo": arquivo.name,
            "data": quando,
            "total": total,
            "nivel_aval": faixa(total, com),
            "comunicacao": com,
            "alcance": fm.get("alcance", "").strip() or "nao-informado",
            "confianca": num(fm.get("confianca_declarada"), 0),
            "tema": fm.get("tema", "").strip(),
        })

    for lista in por_eixo.values():
        lista.sort(key=lambda a: a["data"])
    return por_eixo, descartadas, portao_fechado


def consolidar_eixo(avaliacoes, hoje):
    """Aplica as duas regras: sobe com 2 consecutivas, nunca desce, expira em 90 dias."""
    if not avaliacoes:
        return {"nivel": 0, "status": "nunca_avaliado", "avaliacoes": 0}

    # Sobe so com 2 avaliacoes consecutivas na faixa; nunca desce.
    confirmado = 0
    for anterior, atual in zip(avaliacoes, avaliacoes[1:]):
        par = min(anterior["nivel_aval"], atual["nivel_aval"])
        confirmado = max(confirmado, par)

    ultima = avaliacoes[-1]
    provisorio = len(avaliacoes) == 1 or confirmado < ultima["nivel_aval"]
    expira = ultima["data"] + timedelta(days=EXPIRA_DIAS)

    if confirmado == 0:
        nivel, status = ultima["nivel_aval"], "provisorio"
    elif hoje > expira:
        nivel, status = confirmado, "nao_verificado"
    else:
        nivel, status = confirmado, "provisorio" if provisorio else "verificado"

    calibracoes = [a["confianca"] - a["total"] / 4 for a in avaliacoes]
    # Reversed: em caso de empate, most_common desempata pela ordem de insercao,
    # entao a avaliacao mais recente ganha.
    alcances = Counter(a["alcance"] for a in reversed(avaliacoes))

    return {
        "nivel": nivel,
        "nivel_nome": NIVEIS.get(nivel, "-"),
        "status": status,
        "ultima_avaliacao": ultima["data"].isoformat(),
        "expira": expira.isoformat(),
        "avaliacoes": len(avaliacoes),
        "historico_notas": [a["total"] for a in avaliacoes],
        "ultima_nota_nivel": ultima["nivel_aval"],
        "alcance_tipico": alcances.most_common(1)[0][0],
        "calibracao_media": round(sum(calibracoes) / len(calibracoes), 2),
    }


def ler_calibracao(valor):
    if valor >= 1.0:
        return "excesso de confianca"
    if valor <= -1.0:
        return "subconfianca"
    return "calibrado"


def escrever_md(nome, baseline, pasta):
    eixos = baseline["eixos"]
    linhas = [
        f"# Baseline — {nome}",
        "",
        f"Gerado em {baseline['atualizado']} por `recalcular_baseline.py`.",
        "**Nao edite este arquivo.** Ele e derivado de `avaliacoes/pontuadas/`.",
        "",
        f"- Avaliacoes validas: **{baseline['avaliacoes_validas']}**",
        f"- Avaliacoes com portao fechado (nao contam): **{baseline['avaliacoes_portao_fechado']}**",
        "",
    ]

    for grupo, nomes in EIXOS.items():
        linhas += [f"## {grupo}", "",
                   "| Eixo | Nivel | Status | Ultima | Notas | Alcance | Calibracao |",
                   "|---|---|---|---|---|---|---|"]
        for eixo in nomes:
            d = eixos[eixo]
            if d["status"] == "nunca_avaliado":
                linhas.append(f"| `{eixo}` | — | nunca avaliado | — | — | — | — |")
                continue
            notas = ", ".join(str(n) for n in d["historico_notas"][-3:])
            cal = d["calibracao_media"]
            linhas.append(
                f"| `{eixo}` | **N{d['nivel']}** {d['nivel_nome']} | {d['status']} "
                f"| {d['ultima_avaliacao']} | {notas} | {d['alcance_tipico']} "
                f"| {cal:+.2f} ({ler_calibracao(cal)}) |"
            )
        linhas.append("")

    pendentes = [e for e, d in eixos.items() if d["status"] == "nao_verificado"]
    provisorios = [e for e, d in eixos.items() if d["status"] == "provisorio"]
    nunca = [e for e, d in eixos.items() if d["status"] == "nunca_avaliado"]

    linhas += ["## Leitura", ""]
    if pendentes:
        linhas.append(f"- **Expirados (>{EXPIRA_DIAS}d), precisam revalidacao:** "
                      + ", ".join(f"`{e}`" for e in pendentes))
    if provisorios:
        linhas.append("- **Provisorios (nivel nao confirmado por 2 avaliacoes consecutivas "
                      "na mesma faixa):** " + ", ".join(f"`{e}`" for e in provisorios))
    if nunca:
        linhas.append("- **Nunca avaliados:** " + ", ".join(f"`{e}`" for e in nunca))

    micro = [e for e, d in eixos.items() if d.get("alcance_tipico") == "micro"]
    if micro:
        linhas.append("- **Alcance travado no micro:** " + ", ".join(f"`{e}`" for e in micro)
                      + " — sabe tecnica, nao sobe ao negocio. De caso, nao teoria.")

    com = eixos.get("comunicacao", {})
    if com.get("nivel", 0) and com["nivel"] <= 3:
        linhas.append(f"- **Gargalo global:** `comunicacao` em N{com['nivel']}. Como nivel so sobe "
                      "por audio avaliado, isso trava TODOS os eixos. Prioridade.")

    linhas.append("")
    (pasta / "baseline.md").write_text("\n".join(linhas), encoding="utf-8")


def processar(nome):
    pasta = RAIZ / nome
    if not pasta.is_dir():
        print(f"erro: analista '{nome}' nao existe em {RAIZ}")
        return None

    hoje = date.today()
    por_eixo, descartadas, fechadas = carregar_avaliacoes(pasta)
    eixos = {e: consolidar_eixo(por_eixo.get(e, []), hoje) for e in TODOS_EIXOS}
    validas = sum(d["avaliacoes"] for d in eixos.values())

    baseline = {
        "analista": nome,
        "atualizado": hoje.isoformat(),
        "avaliacoes_validas": validas,
        "avaliacoes_portao_fechado": fechadas,
        "avaliacoes_descartadas": descartadas,
        "eixos": eixos,
    }

    (pasta / "baseline.json").write_text(
        json.dumps(baseline, indent=2, ensure_ascii=False), encoding="utf-8")
    escrever_md(nome, baseline, pasta)
    print(f"{nome}: {validas} avaliacao(oes) valida(s), {fechadas} com portao fechado "
          f"-> baseline.json + baseline.md")
    return baseline


def consolidar_time():
    nomes = sorted(p.name for p in RAIZ.iterdir()
                   if p.is_dir() and not p.name.startswith("_"))
    if not nomes:
        print(f"nenhum analista em {RAIZ}")
        return

    baselines = [b for b in (processar(n) for n in nomes) if b]
    linhas = [
        "# Consolidado do time",
        "",
        f"Gerado em {date.today().isoformat()}. Derivado dos `baseline.json` individuais.",
        "",
        "| Analista | Avaliacoes | Eixos verificados | Eixos nunca avaliados | Nivel medio (B) |",
        "|---|---|---|---|---|",
    ]
    for b in baselines:
        eixos = b["eixos"]
        verificados = sum(1 for d in eixos.values() if d["status"] == "verificado")
        nunca = sum(1 for d in eixos.values() if d["status"] == "nunca_avaliado")
        grupo_b = [eixos[e]["nivel"] for e in EIXOS["B - Pratica analitica"]
                   if eixos[e]["nivel"]]
        media = f"{sum(grupo_b) / len(grupo_b):.1f}" if grupo_b else "—"
        linhas.append(f"| {b['analista']} | {b['avaliacoes_validas']} | {verificados} "
                      f"| {nunca} | {media} |")

    linhas += ["", "## Eixos mais fracos do time", ""]
    agregado = {}
    for eixo in TODOS_EIXOS:
        notas = [b["eixos"][eixo]["nivel"] for b in baselines
                 if b["eixos"][eixo]["nivel"]]
        if notas:
            agregado[eixo] = sum(notas) / len(notas)
    for eixo, media in sorted(agregado.items(), key=lambda x: x[1])[:5]:
        linhas.append(f"- `{eixo}`: media N{media:.1f}")

    sem_dado = [e for e in TODOS_EIXOS if e not in agregado]
    if sem_dado:
        linhas += ["", "## Pontos cegos do time (ninguem avaliado)", "",
                   ", ".join(f"`{e}`" for e in sem_dado)]

    linhas.append("")
    destino = RAIZ / "_time" / "consolidado.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(f"consolidado do time -> {destino}")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    print(f"dados: {RAIZ}")
    if sys.argv[1] == "--time":
        consolidar_time()
    elif processar(sys.argv[1]) is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
