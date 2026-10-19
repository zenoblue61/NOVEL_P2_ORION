# PowerShell 용 훅 설치. 저장소 루트에서 실행: .\scripts\install_hooks.ps1
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
if (-not (Test-Path ".git")) { Write-Host "먼저 git init 을 실행하라."; exit 1 }
Copy-Item "scripts\hooks\pre-commit" ".git\hooks\pre-commit" -Force
git config core.quotepath false
git config core.autocrlf false
Write-Host "pre-commit 훅 설치 완료."
