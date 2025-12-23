# ==================
# NARZĘDZIA STARTOWE
# ==================
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
            "param_type": "domain",
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


# DB_PATH = Path("netsechub.db")
# db_client = DBClient.DBClient(DB_PATH)
# db_client.init_db_and_migrate(TOOLS_DB, section_emoji)