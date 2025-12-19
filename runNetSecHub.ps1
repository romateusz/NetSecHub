Write-Host "--------------------------------------" -ForegroundColor Cyan
Write-Host " Uruchamiam NetSecHub..."               -ForegroundColor Cyan
Write-Host "--------------------------------------" -ForegroundColor Cyan

# Uruchomienie aplikacji przez uv
uv run streamlit run NetSecHub.py

# Zatrzymanie okna po zakończeniu
Read-Host "Naciśnij Enter, aby zakończyć"