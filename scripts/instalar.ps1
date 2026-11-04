<#
.SYNOPSIS
    Instala a skill cyber-mentor para o usuario atual. Idempotente.

.DESCRIPTION
    Nao existe local de skills no nivel da maquina: o Claude Code procura em
    ~/.claude/skills (usuario) e <projeto>/.claude/skills (projeto). Portanto cobrir
    "todo o ambiente" significa rodar este script no contexto de cada usuario -- via
    logon script, GPO, Intune, ou a mao.

    Dois modos:
      Copia    (padrao) copia o nucleo para ~/.claude/skills/cyber-mentor.
               E o modo de distribuicao: cada maquina fica com a propria copia.
      Junction cria um link para o nucleo onde ele ja esta.
               E o modo de autoria: uma fonte de verdade so, editavel no lugar.

.PARAMETER Modo
    Copia (padrao) ou Junction.

.PARAMETER Dados
    Pasta de dados do analista. Grava em CYBER_MENTOR_DADOS (escopo User).
    Se omitido e a variavel nao existir, o script apenas avisa.

.PARAMETER Destino
    Pasta de skills de destino. Padrao: ~/.claude/skills

.PARAMETER Force
    Substitui uma instalacao existente.

.EXAMPLE
    .\instalar.ps1
    Instala por copia em ~/.claude/skills/cyber-mentor.

.EXAMPLE
    .\instalar.ps1 -Modo Junction -Dados "$HOME\cyber-mentor-dados"
    Modo autoria, e define a pasta de dados de forma permanente.

.EXAMPLE
    .\instalar.ps1 -Force -Dados "D:\soc\dados"
    Reinstala sobrescrevendo.
#>
param(
    [ValidateSet('Copia', 'Junction')]
    [string]$Modo = 'Copia',

    [string]$Dados,

    [string]$Destino = (Join-Path $HOME '.claude\skills'),

    [switch]$Force
)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------- origem
# $PSScriptRoot nao resolve junction; resolvemos para achar o nucleo real.
$nucleo = Split-Path -Parent $PSScriptRoot
$alvo = [System.IO.Directory]::ResolveLinkTarget($nucleo, $true)
if ($alvo) { $nucleo = $alvo.FullName }

if (-not (Test-Path (Join-Path $nucleo 'SKILL.md'))) {
    Write-Host "erro: nao achei SKILL.md em $nucleo" -ForegroundColor Red
    Write-Host "Rode este script de dentro de cyber-mentor\scripts\."
    exit 1
}

$destinoSkill = Join-Path $Destino 'cyber-mentor'

Write-Host "origem:  $nucleo"
Write-Host "destino: $destinoSkill"
Write-Host "modo:    $Modo"
Write-Host ""

# ---------------------------------------------------------------- guardas
if ($nucleo -like '*\.claude\*') {
    Write-Host "erro: a origem esta dentro de .claude ($nucleo)." -ForegroundColor Red
    Write-Host "Mantenha o nucleo fora da arvore de skills e instale a partir de la."
    exit 1
}

if ((Resolve-Path $nucleo).Path.TrimEnd('\') -eq $destinoSkill.TrimEnd('\')) {
    Write-Host "erro: origem e destino sao a mesma pasta." -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------- limpeza do destino
$jaOk = $false
if (Test-Path $destinoSkill) {
    $item = Get-Item -LiteralPath $destinoSkill -Force
    $ehLink = $item.Attributes -band [System.IO.FileAttributes]::ReparsePoint

    if ($ehLink -and $Modo -eq 'Junction') {
        $atual = [System.IO.Directory]::ResolveLinkTarget($destinoSkill, $true)
        if ($atual -and $atual.FullName.TrimEnd('\') -eq $nucleo.TrimEnd('\')) {
            Write-Host "ja instalado por junction apontando para a origem. Nada a fazer." -ForegroundColor Green
            $jaOk = $true
        }
    }

    if (-not $jaOk) {
        if (-not $Force) {
            Write-Host "destino ja existe. Use -Force para substituir." -ForegroundColor Yellow
            exit 1
        }
        if ($ehLink) {
            # CRITICO: nunca use Remove-Item -Recurse num reparse point -- versoes
            # antigas do PowerShell apagam o CONTEUDO do alvo, ou seja, o seu nucleo.
            # Delete() nao recursivo remove apenas o link.
            [System.IO.Directory]::Delete($destinoSkill, $false)
            Write-Host "link anterior removido (conteudo da origem intacto)"
        }
        else {
            Remove-Item -LiteralPath $destinoSkill -Recurse -Force
            Write-Host "copia anterior removida"
        }
    }
}

# ---------------------------------------------------------------- instalacao
if (-not $jaOk) {
    New-Item -ItemType Directory -Force -Path $Destino | Out-Null

    if ($Modo -eq 'Junction') {
        New-Item -ItemType Junction -Path $destinoSkill -Target $nucleo | Out-Null
        Write-Host "junction criada" -ForegroundColor Green
    }
    else {
        Copy-Item -LiteralPath $nucleo -Destination $destinoSkill -Recurse
        Write-Host "nucleo copiado" -ForegroundColor Green
    }
}

# ---------------------------------------------------------------- pasta de dados
if ($Dados) {
    [Environment]::SetEnvironmentVariable('CYBER_MENTOR_DADOS', $Dados, 'User')
    $env:CYBER_MENTOR_DADOS = $Dados
    New-Item -ItemType Directory -Force -Path $Dados | Out-Null
    Set-Content -Path (Join-Path $Dados '.gitignore') -Value "*`n!.gitignore" -Encoding UTF8
    Write-Host "CYBER_MENTOR_DADOS = $Dados  (escopo User)" -ForegroundColor Green
}
elseif (-not $env:CYBER_MENTOR_DADOS) {
    Write-Host "aviso: CYBER_MENTOR_DADOS nao definida." -ForegroundColor Yellow
    Write-Host "       A skill vai procurar <pasta atual>\dados-analistas e depois o relativo ao nucleo."
    Write-Host "       Para fixar:  .\instalar.ps1 -Dados `"`$HOME\cyber-mentor-dados`" -Force"
}

# ---------------------------------------------------------------- verificacao
Write-Host ""
Write-Host "--- verificacao ---"

$skillMd = Join-Path $destinoSkill 'SKILL.md'
if (Test-Path $skillMd) {
    $nome = (Select-String -Path $skillMd -Pattern '^name:\s*(.+)$').Matches.Groups[1].Value
    Write-Host "SKILL.md legivel no destino, name: $nome" -ForegroundColor Green
}
else {
    Write-Host "FALHA: SKILL.md nao esta legivel no destino" -ForegroundColor Red
    exit 1
}

$faltando = @()
foreach ($p in @('references', 'templates', 'scripts', 'cenarios')) {
    if (-not (Test-Path (Join-Path $destinoSkill $p))) { $faltando += $p }
}
if ($faltando.Count) {
    Write-Host "FALHA: faltam pastas no destino: $($faltando -join ', ')" -ForegroundColor Red
    exit 1
}
Write-Host "estrutura completa (references, templates, scripts, cenarios)" -ForegroundColor Green

$py = Get-Command python -ErrorAction SilentlyContinue
if ($py) { Write-Host "python encontrado: $($py.Source)" -ForegroundColor Green }
else {
    Write-Host "aviso: python nao encontrado no PATH." -ForegroundColor Yellow
    Write-Host "       Todos os modos funcionam; so o baseline automatico fica indisponivel."
}

$temGabarito = @(Get-ChildItem $destinoSkill -Recurse -Filter 'gabarito-raciocinio.md' -ErrorAction SilentlyContinue).Count
if ($temGabarito -gt 0) {
    Write-Host ""
    Write-Host "atencao: este pacote contem $temGabarito gabarito(s) de caso." -ForegroundColor Yellow
    Write-Host "         E o pacote de MENTORIA. Para self-service, distribua o pacote gerado"
    Write-Host "         por empacotar.ps1 -SelfService, que remove os gabaritos."
}

Write-Host ""
Write-Host "Instalado. Abra uma sessao NOVA do Claude Code -- a skill nao entra em sessao ja aberta." -ForegroundColor Cyan
Write-Host "Depois:  .\scripts\novo-analista.ps1 -Nome <seu-nome>"
