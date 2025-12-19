#!/bin/bash
echo "--------------------------------------"
echo "Uruchamiam NetSecHub..."
echo "--------------------------------------"

# Uruchomienie aplikacji przez uv
uv run streamlit run NetSecHub.py

# Zatrzymanie okna po zakończeniu
read -p "Naciśnij [Enter], aby zamknąć..."