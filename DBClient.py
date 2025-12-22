import sqlite3
import csv


class DBClient:
    def __init__(self, db_path):
        self.db_path = db_path


    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn


    def init_db_and_migrate(self, tools_db, section_emoji):
        conn = self.get_connection()
        cur = conn.cursor()

        # Tworzenie tabel
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                emoji TEXT,
                order_index INTEGER,
                is_active INTEGER DEFAULT 1
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id INTEGER,
                name TEXT,
                description TEXT,
                url_template TEXT,
                param_type TEXT,
                order_index INTEGER,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (section_id) REFERENCES sections(id)
            )
        """)

        # Sprawdzenie czy są już dane
        cur.execute("SELECT COUNT(*) FROM sections")
        if cur.fetchone()[0] > 0:
            conn.close()
            return  # Baza już wypełniona

        # Migracja danych
        for s_idx, (section_name, tools) in enumerate(tools_db.items()):
            emoji = section_emoji.get(section_name, "📁")

            cur.execute(
                "INSERT INTO sections (name, emoji, order_index) VALUES (?, ?, ?)",
                (section_name, emoji, s_idx)
            )
            section_id = cur.lastrowid

            for t_idx, tool in enumerate(tools):
                cur.execute("""
                    INSERT INTO tools (
                        section_id, name, description, url_template,
                        param_type, order_index
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    section_id,
                    tool["name"],
                    tool['desc'],
                    tool["url_template"],
                    tool["param_type"],
                    t_idx
                ))

        conn.commit()
        conn.close()


    def tool_exists(self, name, section_id):
        """Sprawdza, czy w danej sekcji istnieje już narzędzie o takiej nazwie."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM tools WHERE name = ? AND section_id = ?", (name, section_id))
        exists = cur.fetchone() is not None
        conn.close()
        return exists


    def import_from_csv(self, file_content):
        """Importuje dane z CSV, pomijając duplikaty w obrębie tej samej sekcji."""
        decoded_file = file_content.getvalue().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file, delimiter=';')
        
        conn = self.get_connection()
        cur = conn.cursor()
        skipped_tools = []
        
        try:
            for row in reader:
                # 1. Sprawdź/Dodaj sekcję
                cur.execute("SELECT id FROM sections WHERE name = ?", (row['Sekcja'],))
                res = cur.fetchone()
                if res:
                    section_id = res['id']
                else:
                    cur.execute("INSERT INTO sections (name, emoji, order_index) VALUES (?, ?, ?)",
                                (row['Sekcja'], row['Emoji'], 0))
                    section_id = cur.lastrowid
                
                # 2. SPRAWDZENIE DUPLIKATU
                # Sprawdzamy, czy w tej sekcji jest już narzędzie o tej samej nazwie
                cur.execute("SELECT id FROM tools WHERE name = ? AND section_id = ?", 
                            (row['Nazwa Narzędzia'], section_id))
                
                if cur.fetchone():
                    skipped_tools.append(f"{row['Nazwa Narzędzia']} ({row['Sekcja']})")
                    continue # Przejdź do następnego rekordu bez dodawania
                
                # 3. Dodaj narzędzie
                cur.execute("""
                    INSERT INTO tools (section_id, name, description, url_template, param_type, order_index)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (section_id, row['Nazwa Narzędzia'], row['Opis'], row['URL Template'], row['Parametr'], 0))
                
            conn.commit()
            return True, skipped_tools
        except Exception as e:
            print(f"Błąd importu: {e}")
            return False, []
        finally:
            conn.close()



    def load_sections(self):
        conn = self.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, emoji
            FROM sections
            WHERE is_active = 1
            ORDER BY order_index
        """)
        sections = cur.fetchall()
        conn.close()
        return sections


    def load_tools_for_section(self, section_name):
        conn = self.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT t.*
            FROM tools t
            JOIN sections s ON s.id = t.section_id
            WHERE s.name = ?
            AND t.is_active = 1
            ORDER BY t.order_index
        """, (section_name,))

        tools = cur.fetchall()
        conn.close()
        return tools

    def load_all_sections(self):
        """Pobiera wszystkie sekcje, nawet te nieaktywne (używane w Kreatorze)"""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, emoji, is_active FROM sections ORDER BY order_index")
        sections = cur.fetchall()
        conn.close()
        return sections

    def load_all_tools_for_section(self, section_name):
        """Pobiera wszystkie narzędzia dla sekcji, nawet nieaktywne (używane w Kreatorze)"""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT t.*
            FROM tools t
            JOIN sections s ON s.id = t.section_id
            WHERE s.name = ?
            ORDER BY t.order_index
        """, (section_name,))
        tools = cur.fetchall()
        conn.close()
        return tools
    

    # --- ZARZĄDZANIE SEKCJAMI ---
    def add_section(self, name, emoji, order_index=0):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO sections (name, emoji, order_index) VALUES (?, ?, ?)", 
                        (name, emoji, order_index))
            conn.commit()
        finally:
            conn.close()

    # W DBClient.py zastąp starą metodę update_section:
    def update_section(self, section_id, name, emoji, is_active):
        conn = self.get_connection()
        cur = conn.cursor()
        # Teraz przekazujemy dokładnie 4 wartości do 4 znaków zapytania
        cur.execute("""
            UPDATE sections 
            SET name = ?, emoji = ?, is_active = ? 
            WHERE id = ?
        """, (name, emoji, int(is_active), section_id))
        conn.commit()
        conn.close()

    # --- ZARZĄDZANIE NARZĘDZIAMI ---
    def add_tool(self, section_id, name, description, url_template, param_type, order_index=0):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tools (section_id, name, description, url_template, param_type, order_index)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (section_id, name, description, url_template, param_type, order_index))
        conn.commit()
        conn.close()

    def update_tool(self, tool_id, name, description, url_template, param_type, is_active):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE tools 
            SET name = ?, description = ?, url_template = ?, param_type = ?, is_active = ?
            WHERE id = ?
        """, (name, description, url_template, param_type, int(is_active), tool_id))
        conn.commit()
        conn.close()

    # --- USUWANIE SEKCJI ---
    def delete_section_soft(self, section_id):
        """Dezaktywacja sekcji (Soft Delete)"""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE sections SET is_active = 0 WHERE id = ?", (section_id,))
        conn.commit()
        conn.close()

    def delete_section_hard(self, section_id):
        """Całkowite usunięcie sekcji i jej narzędzi z bazy"""
        conn = self.get_connection()
        cur = conn.cursor()
        # Najpierw usuwamy narzędzia przypisane do sekcji (klucz obcy)
        cur.execute("DELETE FROM tools WHERE section_id = ?", (section_id,))
        cur.execute("DELETE FROM sections WHERE id = ?", (section_id,))
        conn.commit()
        conn.close()

    # --- USUWANIE NARZĘDZI ---
    def delete_tool_hard(self, tool_id):
        """Całkowite usunięcie konkretnego narzędzia"""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tools WHERE id = ?", (tool_id,))
        conn.commit()
        conn.close()