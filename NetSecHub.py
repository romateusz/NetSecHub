import streamlit as st

# =====================
# KONFIGURACJA STRONY
# =====================
st.set_page_config(
    page_title="NetSecHub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================
# CSS DLA PRZYCISKÓW
# =====================
st.markdown("""
    <style>
    /* Styl podstawowy dla link_button */
    div[data-testid="stLinkButton"] a {
        background-color: #e0f2f7 !important;
        color: #000000 !important;
        border: 1px solid #add8e6;
        transition: all 0.3s ease-in-out;
        font-weight: bold;
    }

    /* Efekt po najechaniu myszką (Hover) */
    div[data-testid="stLinkButton"] a:hover {
        background-color: #0F2866 !important;
        color: #ffffff !important;
        transform: scale(1.02);
        border: 1.5px solid #ffffff;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================
# BAZA DANYCH NARZĘDZI 
# =====================
# Klucz słownika to nazwa sekcji w menu.
# Wartość to lista narzędzi w tej sekcji.
# 'url_template': Użyj {}, gdzie ma zostać wstawiony parametr (IP lub Domena)
# 'param_type': Określa, którego pola wejściowego użyć ('ip', 'domain', lub 'both')

TOOLS_DB = {
    "🔍 DNS & Whois": [
        {
            "name": "DNSDumpster",
            "desc": "Mapowanie DNS i rekonesans subdomen.",
            "url_template": "https://dnsdumpster.com/",
            "param_type": "none",
        },
        {
            "name": "ViewDNS.info",
            "desc": "Obszerny zestaw narzędzi DNS (Whois, IP History, etc.).",
            "url_template": "https://viewdns.info/reverseip/?host={}&t=1",
            "param_type": "both",
        },
         {
            "name": "Who.is",
            "desc": "Standardowe sprawdzenie WHOIS.",
            "url_template": "https://who.is/whois/{}",
            "param_type": "both",
        },
    ],
    "🦠 Threat Intelligence": [
        {
            "name": "VirusTotal (Search)",
            "desc": "Sprawdź reputację IP, domeny lub hasha pliku.",
            "url_template": "https://www.virustotal.com/gui/search/{}",
            "param_type": "both",
        },
        {
            "name": "AbuseIPDB",
            "desc": "Sprawdź zgłoszenia nadużyć dla danego adresu IP.",
            "url_template": "https://www.abuseipdb.com/check/{}",
            "param_type": "ip",
        },
        {
            "name": "Cisco Talos Reputation",
            "desc": "Oficjalne dane o reputacji od Cisco.",
            "url_template": "https://talosintelligence.com/reputation_center/lookup?search={}",
            "param_type": "ip",
        },
        {
            "name": "OTX AlienVault",
            "desc": "Open Threat Exchange - wskaźniki kompromitacji.",
            "url_template": "https://otx.alienvault.com/indicator/ip/{}",
            "param_type": "ip",
        },
    ],
    "📡 Skanowanie i Techniczne": [
        {
            "name": "Shodan (Host)",
            "desc": "Wyszukiwarka urządzeń podłączonych do internetu (IoT, serwery).",
            "url_template": "https://www.shodan.io/host/{}",
            "param_type": "ip",
        },
        {
            "name": "Censys Search",
            "desc": "Analiza hostów i certyfikatów.",
            "url_template": "https://search.censys.io/hosts/{}",
            "param_type": "ip",
        },
        {
            "name": "SSL Labs Server Test",
            "desc": "Dogłębna analiza konfiguracji SSL/TLS serwera.",
            "url_template": "https://www.ssllabs.com/ssltest/analyze.html?d={}&hideResults=on",
            "param_type": "domain",
        },
        {
            "name": "CRT.sh (Certificate Logs)",
            "desc": "Wyszukiwanie w logach Certificate Transparency (znajdowanie subdomen).",
            "url_template": "https://crt.sh/?q={}",
            "param_type": "domain",
        }
    ],
    "🏢 Rejestry Internetowe (RIR)": [
        {
            "name": "RIPE NCC (Europa/Bliski Wschód)",
            "desc": "Szczegółowe dane o alokacji IP w naszym regionie.",
            "url_template": "https://apps.db.ripe.net/db-web-ui/query?searchtext={}",
            "param_type": "ip",
        },
        {
            "name": "ARIN (Ameryka Płn.)",
            "desc": "Dane WHOIS dla Ameryki Północnej.",
            "url_template": "https://search.arin.net/rdap/?query={}",
            "param_type": "ip",
        },
         {
            "name": "BGP Hurricane Electric",
            "desc": "Świetne narzędzie do analizy tras BGP i powiązań ASN.",
            "url_template": "https://bgp.he.net/ip/{}",
            "param_type": "ip",
        },
    ]
}


section_emoji = {
    "🔍 DNS & Whois": "🔍",
    "🦠 Threat Intelligence": "🦠",
    "📡 Skanowanie i Techniczne": "📡",
    "🏢 Rejestry Internetowe (RIR)": "🏢",
}

# ======================
# INTERFEJS UŻYTKOWNIKA
# ======================
with st.sidebar:
    st.title("🛡️ NetSec Hub")
    st.markdown("---")
    st.markdown("**Centrum operacyjne** dla sieciowców i bezpieczników.")
    st.markdown("Wybierz kategorię z menu poniżej.")
    
    section_options = ["🏠 Landing Page"] + list(TOOLS_DB.keys())
    selected_section = st.radio("Nawigacja:", section_options)
    
    st.markdown("---")
    st.info("💡 Wskazówka: Linki otwierają się w nowych kartach.")


# ========================
# LOGIKA GŁÓWNA APLIKACJI
# ========================

# --- LANDING PAGE ---
if selected_section == "🏠 Landing Page":
    st.title("Witaj w NetSec Hub")
    st.markdown("""
    To narzędzie agreguje przydatne serwisy zewnętrzne służące do analizy sieciowej, 
    rekonesansu (OSINT) i threat intelligence.
    
    ### Jak używać?
    1. **Wybierz kategorię** z menu po lewej stronie (np. *DNS & Whois*).
    2. **Wpisz parametry** na górze strony (Adres IP lub Domenę).
    3. Przejrzyj listę dostępnych narzędzi.
    4. Kliknij **"Otwórz ↗️"**, aby uruchomić narzędzie z wpisanymi parametrami w nowej karcie.
    
    ---
    Autor: Mateusz Roman
    """)

# --- STRONY TEMATYCZNE ---
else:
    # Tytuł sekcji
    st.title(selected_section)
    st.markdown("---")

    # Pola wejściowe dla IP i Domeny
    st.subheader("Wprowadź parametry")
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        input_ip = st.text_input("Adres IP (IPv4/IPv6):", placeholder="np. 8.8.8.8").strip()
    with col_input2:
        raw_domain = st.text_input("Nazwa Domeny:", placeholder="np. example.com").strip()
        input_domain = raw_domain.replace("https://", "").replace("http://", "").split("/")[0]

    st.markdown("---")
    st.subheader(f"Dostępne narzędzia w wybranej sekcji:")

    # Iteracja po narzędziach i wyświetlanie interfejsu
    tools_list = TOOLS_DB[selected_section]

    for tool in tools_list:
        # Kontener dla każdego narzędzia
        with st.container(border=True):
            # Układ kolumn: Nazwa/Opis | Podgląd Linku | Przycisk Akcji
            col_desc, col_preview, col_action = st.columns([3, 4, 1.5])

            with col_desc:
                st.markdown(f"### {section_emoji[selected_section]} {tool['name']}")
                st.caption(tool['desc'])
                # Informacja, jakiego parametru oczekuje narzędzie
                req_param = tool['param_type']
                badge_color = "blue" if req_param == "ip" else "green" if req_param == "domain" else "orange"
                st.markdown(f":{badge_color}[Wymaga: {req_param.upper()}]")

            # --- Logika generowania linku ---
            generated_url = None
            ready_to_launch = False
            
            # Sprawdza, czy mamy odpowiednie dane dla danego narzędzia
            if tool['param_type'] == 'none':
                 generated_url = tool['url_template']
                 ready_to_launch = True
            elif tool['param_type'] == 'ip' and input_ip:
                 generated_url = tool['url_template'].format(input_ip)
                 ready_to_launch = True
            elif tool['param_type'] == 'domain' and input_domain:
                 generated_url = tool['url_template'].format(input_domain)
                 ready_to_launch = True
            elif tool['param_type'] == 'both':
                # Dla 'both' priorytet ma IP, jeśli podano oba
                if input_ip:
                     generated_url = tool['url_template'].format(input_ip)
                     ready_to_launch = True
                elif input_domain:
                     generated_url = tool['url_template'].format(input_domain)
                     ready_to_launch = True

            with col_preview:
                if ready_to_launch and generated_url:
                    st.markdown("**Podgląd linku:**")
                    # Wyświetla skrócony link, żeby nie zajmował za dużo miejsca
                    st.code(generated_url, language="http")
                elif not input_ip and not input_domain:
                    st.warning("⬆️ Wpisz parametry na górze strony.")
                else:
                    st.error(f"Brak wymaganego parametru: {tool['param_type'].upper()}")

            with col_action:
                st.markdown(" ") 
                st.markdown(" ")
                
                # Unikalny klucz potrzebny dla zwykłego przycisku
                unique_key = f"wait_btn_{tool['name'].replace(' ', '_')}"

                if ready_to_launch and generated_url:
                    st.link_button(
                        "Otwórz ↗️", 
                        generated_url, 
                        type="primary", 
                        use_container_width=True
                    )
                else:
                    st.button(
                        "Oczekiwanie...", 
                        disabled=True, 
                        use_container_width=True, 
                        key=unique_key
                    )