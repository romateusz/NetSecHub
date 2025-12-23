#!/bin/bash
set -e

# Sprawdź czy uv jest zainstalowany
if ! command -v uv &> /dev/null; then
    echo "[ERROR] Narzędzie 'uv' nie jest zainstalowane."
    echo "Zainstaluj je komendą:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Jeśli nie ma folderu .venv, stwórz go i zainstaluj biblioteki
if [ ! -d ".venv" ]; then
    echo "[INFO] Pierwsze uruchomienie - instaluję zależności..."
    uv sync
fi

# Uruchom aplikację
echo "[INFO] Startuję NetSecHub..."
uv run streamlit run ./src/NetSecHub.py