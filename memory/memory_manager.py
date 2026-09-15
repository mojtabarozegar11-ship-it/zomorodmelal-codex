import sqlite3
from pathlib import Path


class MemoryManager:
    def __init__(self, db_path="data/memory.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save(self, category, content):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO memories (category, content) VALUES (?, ?)",
                (category, content)
            )

    def get_all(self):
        with self._connect() as conn:
            return conn.execute(
                "SELECT id, category, content, created_at "
                "FROM memories ORDER BY id DESC"
            ).fetchall()


if __name__ == "__main__":
    memory = MemoryManager()

    memory.save(
        "system",
        "Master Agent memory system initialized."
    )

    print("🧠 Memory Manager فعال شد.")
    print("💾 حافظه دائمی آماده است.")
    print("📚 تعداد رکوردها:", len(memory.get_all()))
