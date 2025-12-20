# 🛡️ NetSecHub

**Autor:** Mateusz Roman (@romateusz)

**NetSecHub** to lekki i szybki dashboard operacyjny zbudowany w Pythonie, przeznaczony dla specjalistów ds. cyberbezpieczeństwa. Agreguje najważniejsze narzędzia OSINT, Threat Intelligence i diagnostyki sieciowej w jednym, interaktywnym interfejsie.


## Główne Funkcje

* **🔍 Rekonesans DNS:** Szybki dostęp do DNSDumpster, WHOIS i rekordów certyfikatów.
* **🦠 Threat Intelligence:** Integracja z AbuseIPDB, VirusTotal oraz Cisco Talos.
* **📡 Skanowanie i OSINT:** Błyskawiczne przejście do wyników Shodan, Censys i CRT.sh.
* **🏢 Rejestry Internetowe (RIR):** Weryfikacja właścicieli, jurysdykcji i danych kontaktowych adresów IP w globalnych bazach.
* **🧩 Kreator Huba** Zarządzanie strukturą aplikacji. Umożliwia deeaktywacje elementów, któr znikają z menu nawigacji, ale zostają w bazie.
* **📥 Szybki Import** Umożliwia szybki import i zmianę sekcji oraz narzędzi.
* **⚙️ Dynamiczne parametry:** Wszystkie linki generują się automatycznie.
* **🎨 Nowoczesny UI:** Responsywne przyciski, komunikaty i czytelny podgląd generowanych linków.

## Instalacja i Uruchomienie

Projekt zarządza zależnościami za pomocą nowoczesnego menedżera pakietów **uv**. Dzięki temu start aplikacji jest bardzo prosty.

```bash
git clone https://github.com/romateusz/NetSecHub.git
cd NetSecHub
```

### Instalacja dla Linux
Instalacja uv (jeśli nie jest zainstalowane)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Należy również dodać uprawnienia do skryptu:

```bash
chmod +x runNetSecHub.sh
```
Uruchomienie aplikacji:

```bash
./runNetSecHub.sh
```

### Instalacja dla Windows
Instalacja uv (jeśli nie posiadasz):

```PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Odblokowanie skryptów (jeśli to Twoje pierwsze uruchomienie skryptu .ps1):

```PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Uruchomienie: Wpisz poniższą komendę lub kliknij prawym przyciskiem myszy na plik i wybierz "Uruchom z PowerShell":

```PowerShell
./runNetSecHub.ps1
```

## Dostęp do aplikacji
Po poprawnym uruchomieniu skryptu, aplikacja będzie dostępna w przeglądarce pod adresem: http://localhost:8222


## Licencja

Projekt jest udostępniony na licencji MIT – szczegóły znajdują się w pliku [LICENSE](LICENSE).


## Zastrzeżenie prawne

To narzędzie zostało stworzone wyłącznie do **legalnych i etycznych testów bezpieczeństwa**, analiz OSINT oraz celów edukacyjnych.

Autor nie ponosi odpowiedzialności za niewłaściwe lub nielegalne użycie oprogramowania.