Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Info($msg) {
    Write-Host "[INFO]  $msg" -ForegroundColor Cyan
}

function Write-ErrorMsg($msg) {
    Write-Host "[ERROR] $msg" -ForegroundColor Red
}

# Sprawdź czy uv jest zainstalowany
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-ErrorMsg "Narzędzie 'uv' nie jest zainstalowane."
    Write-Host "Zainstaluj je poleceniem:"
    Write-Host "  powershell -c `"irm https://astral.sh/uv/install.ps1 | iex`""
    pause
    exit 1
}

# Pierwsze uruchomienie – instalacja zależności
if (!(Test-Path ".venv")) {
    Write-Info "Pierwsze uruchomienie – instaluję zależności..."
    uv sync
}

# Uruchom aplikację
Write-Info "Startuję NetSecHub..."
uv run streamlit run NetSecHub.py
