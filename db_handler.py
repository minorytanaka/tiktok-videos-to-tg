import sqlite3
from contextlib import closing


DB_NAME = "bot.db"



class DBService:

    def init_db(self):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS modes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    value TEXT UNIQUE NOT NULL
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    mode_id INTEGER,
                    FOREIGN KEY (mode_id) REFERENCES modes (id)
                );
            """)
            conn.commit()

    def get_mode_by_name(self, mode_name: str):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.execute("SELECT id FROM modes WHERE value = ?", (mode_name,))
            row = cursor.fetchone()
            return row[0]

    def get_mode_value_by_user(self, user_id: int):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.execute("SELECT mode_id FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            mode_id = row[0]
            cursor = conn.execute("SELECT value FROM modes WHERE id = ?", (mode_id,))
            row = cursor.fetchone()
            return row[0]

    def add_modes(self):
        with sqlite3.connect(DB_NAME) as conn:
            conn.executemany(
                "INSERT OR IGNORE INTO modes (name, value) VALUES (?, ?);",
                [
                    ("Отправка в канал", "CHANNEL"),
                    ("Отправка пользователю", "PRIVATE"),
                ]
            )
            conn.commit()

    def add_user(self, user_id: int, username: str, first_name: str, mode_id: int):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                INSERT INTO users (user_id, username, first_name, mode_id)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = excluded.username,
                    first_name = excluded.first_name,
                    mode_id = excluded.mode_id
            """, (user_id, username, first_name, mode_id))
            conn.commit()
