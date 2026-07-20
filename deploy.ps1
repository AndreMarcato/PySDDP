param(
    [Parameter(Position = 0)]
    [string]$Version,

    [Parameter(Position = 1)]
    [string]$Message,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = $PSScriptRoot
Set-Location $repoRoot

function Assert-Command {
    param([Parameter(Mandatory = $true)] [string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Comando não encontrado no PATH: $Name"
    }
}

Assert-Command -Name 'git'
Assert-Command -Name 'python'

if ([string]::IsNullOrWhiteSpace($Version)) {
    $Version = Read-Host 'Digite a nova versão (ex.: 0.0.66)'
}

if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = "Release $Version"
}

if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Versão inválida: $Version. Use um formato como 0.0.66."
}

$setupPath = Join-Path $repoRoot 'setup.py'
if (-not (Test-Path $setupPath)) {
    throw "Arquivo setup.py não encontrado em $repoRoot"
}

$content = Get-Content -Path $setupPath -Raw
$pattern = '(?m)^VERSION\s*=\s*["''][^"'']+["'']'
$updatedContent = [regex]::Replace($content, $pattern, "VERSION = `"$Version`"", 1)

if ($updatedContent -eq $content) {
    throw 'Não foi possível localizar a linha VERSION em setup.py'
}

Set-Content -Path $setupPath -Value $updatedContent -Encoding utf8
Write-Host "Versão atualizada para $Version em setup.py"

if ($DryRun) {
    Write-Host '[DryRun] git add -A'
    Write-Host '[DryRun] git commit -m "{0}"' -f $Message
    Write-Host '[DryRun] git push origin <branch>'
    Write-Host '[DryRun] git tag {0}' -f $Version
    Write-Host '[DryRun] git push origin {0}' -f $Version
    return
}

git add -A
git commit -m $Message

$branch = git branch --show-current
if ([string]::IsNullOrWhiteSpace($branch)) {
    $branch = 'master'
}

git push origin $branch
git tag $Version
git push origin $Version

Write-Host ''
Write-Host 'Fluxo concluído.'
Write-Host '- Commit enviado para o GitHub'
Write-Host ("- Tag criada e enviada: {0}" -f $Version)
Write-Host '- O CircleCI deve disparar automaticamente após o push da tag'
