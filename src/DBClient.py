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
            return

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
        """Import z zachowaniem kolejności i obsługą polskich znaków"""
        try:
            raw_data = file_content.getvalue()
            try:
                decoded_file = raw_data.decode("utf-8").splitlines()
            except UnicodeDecodeError:
                decoded_file = raw_data.decode("windows-1250").splitlines()

            reader = csv.reader(decoded_file, delimiter=';')
            next(reader) # Pomija nagłówek

            skipped_tools = []
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for row in reader:
                    if len(row) < 6: continue
                    s_name, s_emoji, t_name, t_desc, t_url, t_param = [x.strip() for x in row[:6]]

                    cursor.execute("SELECT id FROM sections WHERE name = ?", (s_name,))
                    res = cursor.fetchone()
                    if res:
                        section_id = res['id']
                    else:
                        cursor.execute("""
                            INSERT INTO sections (name, emoji, order_index, is_active) 
                            VALUES (?, ?, (SELECT COALESCE(MAX(order_index), 0) + 1 FROM sections), 1)
                        """, (s_name, s_emoji))
                        section_id = cursor.lastrowid

                    cursor.execute("SELECT id FROM tools WHERE name = ? AND section_id = ?", (t_name, section_id))
                    if cursor.fetchone():
                        skipped_tools.append(f"{s_name} -> {t_name}")
                        continue

                    cursor.execute("""
                        INSERT INTO tools (section_id, name, description, url_template, param_type, order_index, is_active)
                        VALUES (?, ?, ?, ?, ?, (SELECT COALESCE(MAX(order_index), 0) + 1 FROM tools WHERE section_id = ?), 1)
                    """, (section_id, t_name, t_desc, t_url, t_param.lower(), section_id))
            return True, skipped_tools
        except Exception as e:
            print(f"Błąd: {e}")
            return False, []


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


    def load_all_active_tools(self):
        """Pobiera wszystkie aktywne narzędzia wraz z nazwami ich sekcji."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT t.*, s.name as section_name, s.emoji as section_emoji
            FROM tools t
            JOIN sections s ON s.id = t.section_id
            WHERE t.is_active = 1 AND s.is_active = 1
            ORDER BY s.name, t.name
        """)
        tools = cur.fetchall()
        conn.close()
        return tools


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
    

    def add_section(self, name, emoji):
        """Dodaje sekcję na sam koniec listy"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO sections (name, emoji, order_index, is_active) 
                VALUES (?, ?, (SELECT COALESCE(MAX(order_index), 0) + 1 FROM sections), 1)
            """, (name, emoji))


    def update_section(self, section_id, name, emoji, is_active):
        """Aktualizacja sekcji (teraz bezpieczniejsza dzięki 'with')"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE sections 
                SET name = ?, emoji = ?, is_active = ? 
                WHERE id = ?
            """, (name, emoji, int(is_active), section_id))


    def add_tool(self, section_id, name, description, url_template, param_type):
        """Dodaje narzędzie na koniec listy wewnątrz danej sekcji"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO tools (section_id, name, description, url_template, param_type, order_index, is_active)
                VALUES (?, ?, ?, ?, ?, (SELECT COALESCE(MAX(order_index), 0) + 1 FROM tools WHERE section_id = ?), 1)
            """, (section_id, name, description, url_template, param_type, section_id))


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
        cur.execute("DELETE FROM tools WHERE section_id = ?", (section_id,))
        cur.execute("DELETE FROM sections WHERE id = ?", (section_id,))
        conn.commit()
        conn.close()


    def delete_tool_hard(self, tool_id):
        """Całkowite usunięcie konkretnego narzędzia"""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tools WHERE id = ?", (tool_id,))
        conn.commit()
        conn.close()