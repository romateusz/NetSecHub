from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import markdownStyle as mdS
import DBClient
import ipaddress

if 'history' not in st.session_state:
    st.session_state.history = []

# Globalne "źródło prawdy"
if 'input_ip_val' not in st.session_state:
    st.session_state.input_ip_val = ""
if 'input_dom_val' not in st.session_state:
    st.session_state.input_dom_val = ""

# Klucze konkretnych widgetów
for key in ["lp_ip_input", "lp_dom_input", "sec_ip_input", "sec_dom_input"]:
    if key not in st.session_state:
        st.session_state[key] = ""

def add_to_history(value):
    if value and value not in st.session_state.history:
        st.session_state.history.insert(0, value)
        st.session_state.history = st.session_state.history[:10]

# =====================
# KONFIGURACJA STRONY
# =====================
st.set_page_config(
    page_title="NetSecHub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

mdS.apply_custom_styles()

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "netsechub.db"
db_client = DBClient.DBClient(DB_PATH)


# ======================
# INTERFEJS UŻYTKOWNIKA
# ======================
with st.sidebar:
    st.title("🛡️ NetSec Hub")
    st.markdown("---")
    st.markdown("**🧭 Nawigacja:**") 
    
    sections = db_client.load_sections()
    full_emoji_map = {s["name"]: s["emoji"] for s in sections}
    full_emoji_map["Landing Page"] = "🏠"
    full_emoji_map["Kreator Huba"] = "🧩"
    
    clean_options = ["Landing Page"] + [s["name"] for s in sections] + ["Kreator Huba"]
    
    if 'selected_section' not in st.session_state:
        st.session_state.selected_section = "Landing Page"

    try:
        current_index = clean_options.index(st.session_state.selected_section)
    except ValueError:
        current_index = 0

    selected_section = st.radio(
        label="Nawigacja",
        options=clean_options, 
        index=current_index,
        format_func=lambda x: f"{full_emoji_map.get(x, '📁')} {x}",
        key="navigation_radio",
        label_visibility="collapsed"
    )
    st.session_state.selected_section = selected_section
    st.markdown("---")

    st.markdown("**🕒 Ostatnie wyszukiwania:**") 
    if st.session_state.history:
        for item in st.session_state.history:
            if st.button(f"🔗 {item}", key=f"hist_{item}", use_container_width=True):
                is_ip = False
                try:
                    ipaddress.ip_address(item)
                    is_ip = True
                except ValueError:
                    is_ip = False

                if is_ip:
                    st.session_state.input_ip_val = item
                else:
                    st.session_state.input_dom_val = item

                st.session_state["lp_ip_input"] = st.session_state.input_ip_val
                st.session_state["sec_ip_input"] = st.session_state.input_ip_val
                st.session_state["lp_dom_input"] = st.session_state.input_dom_val
                st.session_state["sec_dom_input"] = st.session_state.input_dom_val
                
                st.session_state.selected_section = "Landing Page"
                st.rerun()
    else:
        st.caption("Brak historii.")
    
    st.markdown("---")
    st.info("💡 ***Wskazówka:*** Ctrl + LPM otwiera narzędzia w tle.")
    st.info("💡 ***Wskazówka:*** Nieaktywne elementy znikają z nawigacji, ale zostają w bazie.")


# ========================
# LOGIKA GŁÓWNA APLIKACJI
# ========================

# --- LANDING PAGE ---
if selected_section == "Landing Page":
    st.title("Witaj w NetSec Hub")
    st.markdown("""
    To narzędzie agreguje przydatne serwisy zewnętrzne służące do analizy sieciowej.
                
    ---
                
    ### Jak używać?
    1. **Wybierz sekcję** z menu nawigacyjnego po lewej stronie (np. *DNS & Whois*).
    2. **Wpisz parametry** na górze strony (Adres IP lub Domenę).
    3. Przejrzyj listę dostępnych narzędzi.
    4. Kliknij **"Otwórz ↗️"** lub **"Otwórz wszystkie aktywne ↗️"**, aby uruchomić narzędzia z wpisanymi parametrami w nowej karcie.
    5. 💡 ***Wskazówka*** Kliknij z wciśniętym klawiszem ***[Ctrl]*** (lub kółkiem myszy), aby otworzyć link w tle i pozostać w panelu.
    
    ---
    **Autor: Mateusz Roman**
    """)

    

# --- CREATOR PAGE ---
elif selected_section == "Kreator Huba":
    st.title("🧩 Kreator Huba")
    st.info("Zarządzaj strukturą aplikacji. Dodawaj, edytuj, importuj lub usuwaj sekcje i narzędzia.")

    tab_sections, tab_tools, tab_import = st.tabs(["📁 Sekcje", "🛠️ Narzędzia", "📥 Import"])

    with tab_import:
        st.subheader("Masowy import narzędzi")
        st.markdown("""
        Wgraj plik CSV przygotowany w Excelu. **Format kolumn:** `Sekcja;Emoji;Nazwa Narzędzia;Opis;URL Template;Parametr`
        """)
        
        uploaded_file = st.file_uploader("Wybierz plik CSV", type="csv")
        
        if uploaded_file is not None:
            if st.button("🚀 Rozpocznij import"):
                success, skipped = db_client.import_from_csv(uploaded_file)
                
                if success:
                    if skipped:
                        st.warning(f"Import zakończony. Pominięto istniejące duplikaty: {', '.join(skipped)}")
                    else:
                        st.success("Wszystkie narzędzia zostały zaimportowane pomyślnie!")

                    if st.button("Odśwież widok"):
                        st.rerun()
                else:
                    st.error("Wystąpił błąd podczas importu. Sprawdź strukturę pliku CSV.")

    all_sections_admin = db_client.load_all_sections()

    with tab_sections:
        st.subheader("➕ Dodaj nową sekcję")
        with st.form("add_section_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            new_name = col1.text_input("Nazwa sekcji")
            new_emoji = col2.text_input("Emoji", value="📁")
            if st.form_submit_button("Dodaj sekcję"):
                if new_name:
                    db_client.add_section(new_name, new_emoji)
                    st.success("Dodano sekcję!")
                    st.rerun()

        st.divider()
        st.subheader("✏️ Edytuj istniejące sekcje")
        
        for s in all_sections_admin:
            status_suffix = "" if s['is_active'] else " (❌NIEAKTYWNA)"
            with st.expander(f"{s['emoji']} {s['name']}{status_suffix}"):
                edit_name = st.text_input("Nazwa", value=s['name'], key=f"sec_n_{s['id']}")
                edit_emoji = st.text_input("Emoji", value=s['emoji'], key=f"sec_e_{s['id']}")
                is_active = st.checkbox("Widoczna w nawigacji (Aktywna)", value=bool(s['is_active']), key=f"sec_a_{s['id']}")
                
                col_save, col_del = st.columns(2)
                with col_save:
                    if st.button("Zapisz zmiany", key=f"save_s_{s['id']}", type="primary"):
                        db_client.update_section(s['id'], edit_name, edit_emoji, is_active)
                        st.success("Zapisano!")
                        st.rerun()
                        
                with col_del:
                    with st.popover("🗑️ USUŃ TRWALE"):
                        st.error("UWAGA: Usunięcie sekcji skasuje też wszystkie jej narzędzia!")
                        c_left, c_mid, c_right = st.columns([1, 5, 1])
                        with c_mid:
                            if st.button("POTWIERDZAM USUNIĘCIE", key=f"conf_del_s_{s['id']}", use_container_width=True):
                                db_client.delete_section_hard(s['id'])
                                st.rerun()

    with tab_tools:
        st.subheader("➕ Dodaj nowe narzędzie")
        with st.form("add_tool_form", clear_on_submit=True):
            sec_names = [s['name'] for s in all_sections_admin]
            sec_emojis = {s['name']: s['emoji'] for s in all_sections_admin}

            target_section = st.selectbox(
                "Wybierz sekcję", 
                options=sec_names,
                format_func=lambda x: f"{sec_emojis.get(x, '📁')} {x}",
                key="add_tool_selectbox"
            )

            t_name = st.text_input("Nazwa narzędzia")
            t_desc = st.text_area("Opis")
            t_url = st.text_input("URL Template (użyj {} dla parametru)")
            t_type = st.selectbox("Typ parametru", ["ip", "domain", "both", "none"])

            if st.form_submit_button("Dodaj narzędzie"):
                    sec_id = next(s['id'] for s in all_sections_admin if s['name'] == target_section)
                    db_client.add_tool(sec_id, t_name, t_desc, t_url, t_type)
                    st.success("Narzędzie dodane!")
                    st.rerun()

        st.divider()
        st.subheader("✏️ Zarządzaj narzędziami")
        
        # Filtrowanie narzędzi
        if all_sections_admin:
            filter_sec = st.selectbox(
                "Wybierz sekcję do edycji narzędzi", 
                options=sec_names,
                format_func=lambda x: f"{sec_emojis.get(x, '📁')} {x}",
                key="manage_tool_selectbox"
            )

            tools_to_edit = db_client.load_all_tools_for_section(filter_sec)

            for t in tools_to_edit:
                t_status = "" if t['is_active'] else " ❌ (UKRYTE)"
                with st.expander(f"🛠️ {t['name']}{t_status}"):
                    edit_t_name = st.text_input("Nazwa", value=t['name'], key=f"t_n_{t['id']}")
                    edit_t_desc = st.text_area("Opis", value=t['description'], key=f"t_d_{t['id']}")
                    edit_t_url = st.text_input("URL Template", value=t['url_template'], key=f"t_u_{t['id']}")
                    edit_t_type = st.selectbox("Typ parametru", ["ip", "domain", "both", "none"], 
                                              index=["ip", "domain", "both", "none"].index(t['param_type']), 
                                              key=f"t_t_{t['id']}")
                    edit_t_active = st.checkbox("Narzędzie aktywne", value=bool(t['is_active']), key=f"t_a_{t['id']}")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Zapisz", key=f"t_save_{t['id']}", type="primary"):
                            db_client.update_tool(t['id'], edit_t_name, edit_t_desc, edit_t_url, edit_t_type, edit_t_active)
                            st.success("Zapisano!")
                            st.rerun()
                    with c2:
                        with st.popover("🗑️ USUŃ"):
                            st.error("UWAGA: Usunięcie narzędzia jest nieodwracalne.")
                            ct_left, ct_mid, ct_right = st.columns([1, 5, 1])
                            with ct_mid:
                                if st.button("POTWIERDZAM USUNIĘCIE", key=f"t_del_{t['id']}", use_container_width=True):
                                    db_client.delete_tool_hard(t['id'])
                                    st.rerun()
        else:
            st.warning("Najpierw dodaj jakąś sekcję!")

            
# --- STRONY TEMATYCZNE ---
else:
    current_emoji = full_emoji_map.get(selected_section, "📁")
    st.title(f"{current_emoji} {selected_section}")
    st.markdown("---")
    tools_list = db_client.load_tools_for_section(selected_section)

    # Obsługa wartości z historii
    default_ip = st.session_state.get('input_ip_val', "")
    default_dom = st.session_state.get('input_dom_val', "")

    # Pola wejściowe dla IP i Domeny
    st.subheader("Wprowadź parametry")
    col_input1, col_input2 = st.columns(2)

    with col_input1:
        input_ip = st.text_input("Adres IP:", key="sec_ip_input").strip()
        
        if input_ip != st.session_state.input_ip_val:
            st.session_state.input_ip_val = input_ip
            st.session_state["lp_ip_input"] = input_ip
            add_to_history(input_ip)

    with col_input2:
        raw_domain = st.text_input("Nazwa Domeny:", key="sec_dom_input").strip()
        input_domain = (raw_domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].lower())
        
        if input_domain != st.session_state.input_dom_val:
            st.session_state.input_dom_val = input_domain
            st.session_state["lp_dom_input"] = input_domain
            add_to_history(input_domain)

    # --- BULK OPEN ---
    urls_to_open = []
    for t in tools_list:
        # Logika generowania linku
        url = None
        if t['param_type'] == 'none': url = t['url_template']
        elif t['param_type'] == 'ip' and input_ip: url = t['url_template'].format(input_ip)
        elif t['param_type'] == 'domain' and input_domain: url = t['url_template'].format(input_domain)
        elif t['param_type'] == 'both':
            if input_ip: url = t['url_template'].format(input_ip)
            elif input_domain: url = t['url_template'].format(input_domain)
        
        if url: urls_to_open.append(url)

    if urls_to_open:
        if st.button(f"Otwórz wszystkie aktywne ({len(urls_to_open)}) ↗️", use_container_width=True):
            # Trick JavaScript do otwarcia wielu kart
            js_code = "".join([f"window.open('{u}', '_blank');" for u in urls_to_open])
            components.html(f"<script>{js_code}</script>", height=0)
            st.info("Zezwól na wyskakujące okienka (pop-ups) w przeglądarce, aby otworzyć wszystkie karty.")

    st.markdown("---")
    st.subheader(f"Dostępne narzędzia w wybranej sekcji:")

    for tool in tools_list:
        # Kontener dla każdego narzędzia
        with st.container(border=True):
            # Układ kolumn: Nazwa/Opis | Podgląd Linku | Przycisk Akcji
            col_desc, col_preview, col_action = st.columns([3, 4, 1.5], vertical_alignment="center")

            with col_desc:
                st.markdown(f"### {current_emoji} {tool['name']}")
                st.caption(tool['description'])
                
                # Logika kolorów i nazw dla parametrów
                req_param = tool['param_type']

                # Słownik tłumaczeń
                param_labels = {
                    "ip": "IP",
                    "domain": "DOMENA",
                    "both": "OBA",
                    "none": "BRAK"
                }

                display_label = param_labels.get(req_param, req_param.upper())

                if req_param == "ip":
                    badge_color = "blue"
                elif req_param == "domain":
                    badge_color = "green"
                elif req_param == "both":
                    badge_color = "orange"
                else:
                    badge_color = "gray"

                st.markdown(f":{badge_color}[Przyjmuje: {display_label}]")

            # --- Logika generowania linku ---
            generated_url = None
            ready_to_launch = False
            
            # Sprawdza, czy odpowiednie dane dla danego narzędzia
            try:
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
            except IndexError:
                # Jeśli w URL Template brakuje {}
                generated_url = "BŁĄD: Brak {} w szablonie URL"
                ready_to_launch = False

            with col_preview:
                if ready_to_launch and generated_url:
                    st.markdown("**Podgląd linku:**")
                    st.code(generated_url, language="http")
                elif not input_ip and not input_domain:
                    st.warning("⬆️ Wpisz parametry na górze strony.")
                else:
                    st.error(f"Brak wymaganego parametru: {tool['param_type'].upper()}")

            with col_action:
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