# 🛡️ NetSecHub

**Autor:** Mateusz Roman (@romateusz)

**NetSecHub** to lekki i szybki dashboard operacyjny zbudowany w Pythonie, przeznaczony dla specjalistów ds. cyberbezpieczeństwa. Agreguje najważniejsze narzędzia OSINT, Threat Intelligence i diagnostyki sieciowej w jednym, interaktywnym interfejsie.


## Główne Funkcje

* **🔍 Rekonesans DNS:** Szybki dostęp do DNSDumpster, WHOIS i rekordów certyfikatów.
* **🦠 Threat Intelligence:** Integracja z AbuseIPDB, VirusTotal oraz Cisco Talos.
* **📡 Skanowanie i OSINT:** Błyskawiczne przejście do wyników Shodan, Censys i CRT.sh.
* **🏢 Rejestry Internetowe (RIR):** Weryfikacja właścicieli, jurysdykcji i danych kontaktowych adresów IP w globalnych bazach.
* **⚙️ Dynamiczne parametry:** Wszystkie linki generują się automatycznie.
* **🎨 Nowoczesny UI:** Responsywne przyciski, komunikaty i czytelny podgląd generowanych linków.

## Instalacja i Uruchomienie

Projekt zarządza zależnościami za pomocą nowoczesnego menedżera pakietów **uv**. Dzięki temu start aplikacji jest bardzo prosty.

```bash
git clone [https://github.com/romateusz/NetSecHub.git](https://github.com/romateusz/NetSecHub.git)
cd NetSecHub
```

### Instalacja dla Linux
Instalacja uv (jeśli nie jest zainstalowane)

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
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
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
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
Po poprawnym uruchomieniu skryptu, dashboard będzie dostępny w przeglądarce pod adresem: http://localhost:8222


## MIT License

Copyright (c) 2025 Mateusz Roman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Zastrzeżenie prawne

To narzędzie zostało stworzone wyłącznie do **legalnych i etycznych testów
bezpieczeństwa**, analiz OSINT oraz celów edukacyjnych.

Autor nie ponosi odpowiedzialności za niewłaściwe lub nielegalne użycie
oprogramowania.