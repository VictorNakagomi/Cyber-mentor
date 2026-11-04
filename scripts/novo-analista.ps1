<#
.SYNOPSIS
    Cria a pasta de dados de um novo analista a partir dos templates.

.DESCRIPTION
    Os dados do analista ficam FORA do nucleo da skill. A pasta de dados e resolvida
    nesta ordem:
      1. variavel de ambiente CYBER_MENTOR_DADOS
      2. <diretorio atual>\dados-analistas, se existir
      3. <pasta do nucleo>\..\dados-analistas

    O nucleo (cyber-mentor\) e distribuivel e igual para todos; os dados sao locais.

.EXAMPLE
    .\novo-analista.ps1 -Nome victor

.EXAMPLE
    $env:CYBER_MENTOR_DADOS = 'D:\soc\dados-analistas'
    .\novo-analista.ps1 -Nome ana
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9][a-z0-9._-]*$')]
    [string]$Nome
)

$ErrorActionPreference = 'Stop'

$nucleo = Split-Path -Parent $PSScriptRoot

# $PSScriptRoot nao resolve junction. Resolvemos o alvo real do nucleo para que este
# script caia na mesma pasta de dados que o recalcular_baseline.py, que resolve sozinho
# via Path.resolve(). Sem isto, os dois scripts divergem rodando do mesmo lugar.
$alvo = [System.IO.Directory]::ResolveLinkTarget($nucleo, $true)
if ($alvo) { $nucleo = $alvo.FullName }

if ($env:CYBER_MENTOR_DADOS) {
    $raiz = $env:CYBER_MENTOR_DADOS
}
elseif (Test-Path (Join-Path (Get-Location) 'dados-analistas')) {
    $raiz = Join-Path (Get-Location) 'dados-analistas'
}
else {
    $raiz = Join-Path (Split-Path -Parent $nucleo) 'dados-analistas'
    if ($raiz -like '*\.claude\*') {
        Write-Host "erro: o caminho de dados caiu dentro de .claude ($raiz)." -ForegroundColor Red
        Write-Host "Defina CYBER_MENTOR_DADOS, ou rode o script a partir da pasta que contem dados-analistas."
        exit 1
    }
}

Write-Host "dados: $raiz" -ForegroundColor DarkGray
$pasta = Join-Path $raiz $Nome

if (Test-Path $pasta) {
    Write-Host "Analista '$Nome' ja existe em $pasta" -ForegroundColor Yellow
    exit 1
}

foreach ($sub in @('sessoes', 'avaliacoes\entrada', 'avaliacoes\pontuadas')) {
    New-Item -ItemType Directory -Force -Path (Join-Path $pasta $sub) | Out-Null
}

$hoje = Get-Date -Format 'yyyy-MM-dd'

# perfil.md vem do template, com nome e data preenchidos
$perfil = Get-Content (Join-Path $nucleo 'templates\perfil.md') -Raw
$perfil = $perfil -replace '<nome>', $Nome -replace '<AAAA-MM-DD>', $hoje
Set-Content -Path (Join-Path $pasta 'perfil.md') -Value $perfil -Encoding UTF8

# lacunas.md tambem vem do template, para nao duplicar o formato em dois lugares
$lacunas = Get-Content (Join-Path $nucleo 'templates\lacunas.md') -Raw
$lacunas = $lacunas -replace '<nome>', $Nome
Set-Content -Path (Join-Path $pasta 'lacunas.md') -Value $lacunas -Encoding UTF8

$gitignore = @"
# Dados de analista nunca vao para o repositorio do nucleo.
*
!.gitignore
"@
Set-Content -Path (Join-Path $raiz '.gitignore') -Value $gitignore -Encoding UTF8

Write-Host "Analista '$Nome' criado em $pasta" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "  1. Preencher perfil.md — a tabela de stack calibra a matriz e os casos"
Write-Host "  2. Pedir a autoavaliacao inicial (perfil.md) ANTES da primeira avaliacao"
Write-Host "  3. Rodar o primeiro caso: cenarios\001-powershell-codificado-financeiro"
