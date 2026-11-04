<#
.SYNOPSIS
    Empacota o nucleo da skill para distribuicao, em dois sabores.

.DESCRIPTION
    Mentoria    pacote completo, com os gabaritos. Para quem CONDUZ as sessoes.
    SelfService remove os gabarito-raciocinio.md. Para o analista que roda sozinho --
                senao a resposta da prova viaja na mesma pasta do aluno.

    O que se perde no SelfService e menos do que parece: a conducao usa caso.md,
    regra.md e evidencias/, e a avaliacao do audio usa a RUBRICA, nao o gabarito
    (a dimensao 3 se apoia no campo `armadilha` do frontmatter do caso). Perde-se
    apenas a comparacao final de caminho.

    Em qualquer modo o script se recusa a empacotar dado de analista.

.PARAMETER Modo
    Mentoria (padrao) ou SelfService.

.PARAMETER Saida
    Caminho do .zip. Padrao: ~/cyber-mentor-<modo>-<data>.zip

.EXAMPLE
    .\empacotar.ps1
.EXAMPLE
    .\empacotar.ps1 -Modo SelfService
#>
param(
    [ValidateSet('Mentoria', 'SelfService')]
    [string]$Modo = 'Mentoria',

    [string]$Saida
)

$ErrorActionPreference = 'Stop'

$nucleo = Split-Path -Parent $PSScriptRoot
$alvo = [System.IO.Directory]::ResolveLinkTarget($nucleo, $true)
if ($alvo) { $nucleo = $alvo.FullName }

if (-not (Test-Path (Join-Path $nucleo 'SKILL.md'))) {
    Write-Host "erro: nao achei SKILL.md em $nucleo" -ForegroundColor Red
    exit 1
}

if (-not $Saida) {
    $data = Get-Date -Format 'yyyy-MM-dd'
    $Saida = Join-Path $HOME "cyber-mentor-$($Modo.ToLower())-$data.zip"
}

$stage = Join-Path $env:TEMP "cm-pack-$([guid]::NewGuid().ToString('N').Substring(0,8))"
Write-Host "origem: $nucleo"
Write-Host "modo:   $Modo"
Write-Host "saida:  $Saida"
Write-Host ""

try {
    Copy-Item -LiteralPath $nucleo -Destination $stage -Recurse

    # ------------------------------------------------ guarda: nada de dado de analista
    $suspeitos = Get-ChildItem $stage -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -in @('baseline.json', 'baseline.md') -or
            $_.FullName -match '\\(dados-analistas|sessoes|avaliacoes|conformidade)\\'
        }

    if ($suspeitos) {
        Write-Host "ABORTADO: o nucleo contem dado de analista." -ForegroundColor Red
        $suspeitos | Select-Object -First 10 -ExpandProperty FullName | ForEach-Object {
            Write-Host "  $($_.Replace($stage, '<nucleo>'))"
        }
        Write-Host ""
        Write-Host "Mova esses arquivos para a pasta de dados antes de empacotar." -ForegroundColor Yellow
        exit 1
    }

    # ------------------------------------------------ self-service: tira os gabaritos
    $removidos = 0
    if ($Modo -eq 'SelfService') {
        Get-ChildItem $stage -Recurse -Filter 'gabarito-raciocinio.md' | ForEach-Object {
            Remove-Item -LiteralPath $_.FullName -Force
            $removidos++
        }
        Write-Host "gabaritos removidos: $removidos" -ForegroundColor Green

        $aviso = @"

---

## Nota deste pacote (self-service)

Os arquivos ``gabarito-raciocinio.md`` foram REMOVIDOS desta copia de proposito: no
self-service o analista e aluno e mentor ao mesmo tempo, e o gabarito na mesma pasta e a
resposta da prova ao lado da prova.

Isto nao limita o uso. A conducao usa ``caso.md``, ``regra.md`` e ``evidencias/``, e a
avaliacao do audio usa a RUBRICA -- nao o gabarito. O que falta aqui e apenas a
comparacao final de caminho, que no self-service seria autoindulgente.

Os blocos ``NOTAS PARA O MENTOR`` dentro das evidencias CONTINUAM no pacote, porque o
Claude precisa deles para conduzir. Sao dicas de conducao, nao gabarito -- mas saiba que
estao la.
"@
        Add-Content -Path (Join-Path $stage 'README.md') -Value $aviso -Encoding UTF8
    }

    # ------------------------------------------------ zip
    if (Test-Path $Saida) { Remove-Item -LiteralPath $Saida -Force }
    Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $Saida -Force

    $tam = [math]::Round((Get-Item $Saida).Length / 1KB, 1)
    $qtd = @(Get-ChildItem $stage -Recurse -File).Count

    Write-Host ""
    Write-Host "pacote pronto: $Saida  ($tam KB, $qtd arquivos)" -ForegroundColor Green
    Write-Host ""
    Write-Host "O destinatario roda:" -ForegroundColor Cyan
    Write-Host "  Expand-Archive '<zip>' -DestinationPath `"`$env:TEMP\cyber-mentor\`""
    Write-Host "  & `"`$env:TEMP\cyber-mentor\scripts\instalar.ps1`" -Dados `"`$HOME\cyber-mentor-dados`""
}
finally {
    if (Test-Path $stage) { Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue }
}
