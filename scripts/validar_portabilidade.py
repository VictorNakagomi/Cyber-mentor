#!/usr/bin/env python3
"""Valida a INTEGRIDADE ESTRUTURAL do nucleo da skill antes de distribuir.

Esta e a Parte 1 da validacao descrita em references/portabilidade.md.
Checa o que um script pode checar: arquivo faltando, referencia morta, arquivo
orfao, caso sem armadilha declarada, gabarito em pacote self-service, dado de
analista dentro do nucleo, caminho de dados caindo em .claude/.

O QUE ELE NAO PROVA: que o modelo obedece as regras duras. Um pacote que passa
100% aqui pode ser inutil no alvo. Para isso rode as 8 sondas comportamentais
de references/portabilidade.md -- nao existe script que as substitua.

Uso:
    python validar_portabilidade.py
    python validar_portabilidade.py --modo selfservice

Sai com codigo 1 em qualquer FALHA. Aviso nao reprova.
Stdlib apenas. Sem dependencias.
"""

import os
import re
import sys
from pathlib import Path

PASTAS_OBRIGATORIAS = ["references", "templates", "scripts", "cenarios"]
ARQUIVOS_CASO = ["caso.md", "regra.md"]
CAMPOS_CASO = ["id", "titulo", "eixos", "nivel_alvo", "armadilha"]
DADO_DE_ANALISTA = ["baseline.json", "baseline.md"]
PASTA_DE_ANALISTA = ["sessoes", "avaliacoes", "dados-analistas", "conformidade"]

falhas = []
avisos = []
oks = []


def falha(msg):
    falhas.append(msg)


def aviso(msg):
    avisos.append(msg)


def ok(msg):
    oks.append(msg)


def nucleo():
    """A pasta do nucleo. resolve() segue junction no Windows."""
    return Path(__file__).resolve().parent.parent


def frontmatter(caminho):
    """Dict raso do frontmatter. Nao e parser YAML: le linhas 'chave: valor'."""
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    if not texto.startswith("---"):
        return {}
    fim = texto.find("\n---", 3)
    if fim < 0:
        return {}
    campos = {}
    for linha in texto[3:fim].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", linha.strip())
        if m:
            campos[m.group(1)] = m.group(2).strip()
    return campos


# ---------------------------------------------------------------- 1. SKILL.md
def checar_skill_md(raiz):
    skill = raiz / "SKILL.md"
    if not skill.is_file():
        falha("SKILL.md nao existe -- sem ele nenhum harness descobre a skill")
        return ""

    texto = skill.read_text(encoding="utf-8", errors="replace")
    campos = frontmatter(skill)
    if not campos:
        falha("SKILL.md sem frontmatter -- o Claude Code nao vai carregar")
        return texto

    for campo in ("name", "description"):
        if not campos.get(campo):
            falha(f"SKILL.md: frontmatter sem {campo}")
    if campos.get("name") and campos["name"] != raiz.name:
        aviso(f"SKILL.md name [{campos['name']}] difere da pasta [{raiz.name}]")
    if len(campos.get("description", "")) < 80:
        aviso("description curta -- a descoberta por intencao fica fraca")
    if campos.get("name") and campos.get("description"):
        ok(f"SKILL.md valido, name: {campos['name']}")
    return texto


# ---------------------------------------------------------------- 2. estrutura
def checar_pastas(raiz):
    faltando = [p for p in PASTAS_OBRIGATORIAS if not (raiz / p).is_dir()]
    if faltando:
        falha(f"pastas obrigatorias faltando: {', '.join(faltando)}")
    else:
        ok(f"estrutura completa ({', '.join(PASTAS_OBRIGATORIAS)})")

    if (raiz / "AGENTS.md").is_file():
        ok("AGENTS.md presente -- harness fora do Claude Code consegue descobrir")
    else:
        aviso("sem AGENTS.md -- Cursor, Codex CLI e afins nao vao achar a skill")


# ------------------------------------------------- 3. referencia morta e orfao
def checar_referencias(raiz, texto_skill):
    corpo = ""
    for arq in raiz.rglob("*.md"):
        corpo += arq.read_text(encoding="utf-8", errors="replace")

    def citados(padrao, texto):
        return set(re.findall(padrao, texto))

    pares = [
        ("references", r"references/([a-z0-9\-]+\.md)", "*.md"),
        ("templates", r"templates/([a-z0-9\-]+\.md)", "*.md"),
        ("scripts", r"scripts[/\\]([a-z0-9_\-]+\.(?:py|ps1))", "*"),
    ]
    for pasta, padrao, glob in pares:
        cit = citados(padrao, corpo)
        existe = {p.name for p in (raiz / pasta).glob(glob) if p.is_file()}
        mortos = sorted(cit - existe)
        if mortos:
            falha(f"{pasta}/ citado e inexistente: {', '.join(mortos)}")
        else:
            ok(f"{len(cit)} arquivo(s) de {pasta}/ citados, todos existem")

    # orfao: existe no disco mas o SKILL.md nao manda carregar em modo nenhum
    no_disco = {p.name for p in (raiz / "references").glob("*.md")}
    no_skill = citados(r"references/([a-z0-9\-]+\.md)", texto_skill)
    orfaos = sorted(no_disco - no_skill)
    if orfaos:
        aviso(f"em references/ mas nao citado no SKILL.md: {', '.join(orfaos)}")

    # pasta no disco que o SKILL.md ignora por completo
    for p in sorted(raiz.iterdir()):
        if p.is_dir() and p.name not in PASTAS_OBRIGATORIAS and not p.name.startswith("."):
            if p.name not in texto_skill:
                aviso(f"pasta [{p.name}/] existe mas o SKILL.md nunca a menciona")


# ------------------------------------------------- 4. dependencia entre skills
def checar_skills_externas(raiz):
    corpo = (raiz / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    nomes = set(re.findall(r"skill\s+`([a-z0-9\-]+)`", corpo))
    nomes.discard("cyber-mentor")
    if nomes:
        aviso(
            f"depende de skill externa: {', '.join(sorted(nomes))} -- "
            "fora do Claude Code isso nao existe; valide a sonda P8"
        )


# ---------------------------------------------------------------- 5. cenarios
def checar_cenarios(raiz, modo):
    casos = [p for p in sorted((raiz / "cenarios").iterdir()) if p.is_dir()]
    if not casos:
        falha("nenhum cenario em cenarios/ -- o modo caso nao tem o que conduzir")
        return

    for caso in casos:
        rotulo = caso.name
        for arq in ARQUIVOS_CASO:
            if not (caso / arq).is_file():
                falha(f"{rotulo}: falta {arq}")

        ev = caso / "evidencias"
        if not ev.is_dir():
            falha(f"{rotulo}: falta evidencias/")
        else:
            if not (ev / "_indisponivel.md").is_file():
                falha(f"{rotulo}: falta evidencias/_indisponivel.md -- a cegueira proposital")
            reais = [p for p in ev.iterdir() if p.is_file() and not p.name.startswith("_")]
            if len(reais) < 3:
                aviso(f"{rotulo}: so {len(reais)} evidencia(s) -- pouco para correlacionar")

        cm = caso / "caso.md"
        if cm.is_file():
            campos = frontmatter(cm)
            faltando = [c for c in CAMPOS_CASO if c not in campos]
            if faltando:
                falha(f"{rotulo}: caso.md sem campo(s) {', '.join(faltando)}")
            arm = campos.get("armadilha", "").lower()
            if "armadilha" in campos and arm not in ("sim", "nao"):
                falha(f"{rotulo}: armadilha deve ser sim ou nao, veio [{arm}]")
            elif arm == "nao":
                aviso(f"{rotulo}: sem armadilha -- dimensao 3 da rubrica nao e mensuravel aqui")

        gab = caso / "gabarito-raciocinio.md"
        if modo == "selfservice" and gab.is_file():
            falha(f"{rotulo}: gabarito presente em pacote selfservice")
        if modo == "mentoria" and not gab.is_file():
            aviso(f"{rotulo}: sem gabarito -- perde a comparacao de caminho")

    ok(f"{len(casos)} cenario(s) verificado(s)")


# --------------------------------------------------- 6. dado de analista vazado
def checar_vazamento(raiz):
    achados = []
    for p in raiz.rglob("*"):
        if p.is_file() and p.name in DADO_DE_ANALISTA:
            achados.append(p)
        elif p.is_dir() and p.name in PASTA_DE_ANALISTA:
            achados.append(p)
    if achados:
        for p in achados[:10]:
            falha(f"dado de analista dentro do nucleo: {p.relative_to(raiz)}")
    else:
        ok("nenhum dado de analista no nucleo")


# ---------------------------------------------------------- 7. pasta de dados
def checar_pasta_dados(raiz):
    env = os.environ.get("CYBER_MENTOR_DADOS")
    if env:
        destino = Path(env).expanduser().resolve()
        origem = "CYBER_MENTOR_DADOS"
    elif (Path.cwd() / "dados-analistas").is_dir():
        destino = (Path.cwd() / "dados-analistas").resolve()
        origem = "diretorio atual"
    else:
        destino = (raiz.parent / "dados-analistas").resolve()
        origem = "relativo ao nucleo"

    if ".claude" in destino.parts:
        falha(f"caminho de dados cai em .claude/ ({destino}) -- quebra nucleo/dados")
    elif destino.is_dir():
        ok(f"pasta de dados: {destino}  (via {origem})")
    else:
        aviso(f"pasta de dados nao existe ainda: {destino}  (via {origem})")


# ---------------------------------------------------------------- relatorio
def main():
    modo = "mentoria"
    if "--modo" in sys.argv:
        i = sys.argv.index("--modo")
        if i + 1 < len(sys.argv):
            modo = sys.argv[i + 1].lower()
    if modo not in ("mentoria", "selfservice"):
        sys.exit("erro: --modo aceita mentoria ou selfservice")

    raiz = nucleo()
    print(f"nucleo: {raiz}")
    print(f"modo:   {modo}")
    print()

    texto_skill = checar_skill_md(raiz)
    checar_pastas(raiz)
    if (raiz / "references").is_dir():
        checar_referencias(raiz, texto_skill)
        checar_skills_externas(raiz)
    if (raiz / "cenarios").is_dir():
        checar_cenarios(raiz, modo)
    checar_vazamento(raiz)
    checar_pasta_dados(raiz)

    for m in oks:
        print(f"  ok     {m}")
    for m in avisos:
        print(f"  aviso  {m}")
    for m in falhas:
        print(f"  FALHA  {m}")

    print()
    print(f"{len(oks)} ok, {len(avisos)} aviso(s), {len(falhas)} falha(s)")
    print()
    if falhas:
        print("estrutura REPROVADA. Corrija antes de distribuir.")
        sys.exit(1)

    print("estrutura aprovada.")
    print()
    print("Isto NAO valida comportamento. Antes de usar um ambiente para AVALIAR alguem,")
    print("rode as 8 sondas de references/portabilidade.md e registre o resultado em")
    print("<raiz de dados>/conformidade/. Avaliacao em ambiente nao validado contamina")
    print("o baseline de forma permanente.")


if __name__ == "__main__":
    main()
