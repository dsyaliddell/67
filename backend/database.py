import sqlite3
import os

class Database:
    """Singleton-класс для работы с SQLite."""
    _instance = None

    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path=None):
        if self._initialized:
            return
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), '..', 'database', 'conference.db'
            )
        self.db_path = os.path.abspath(db_path)
        self._initialized = True

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def execute(self, query, params=()):
        """Выполнить INSERT/UPDATE/DELETE с параметрами."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def fetch_one(self, query, params=()):
        """Получить одну запись с параметрами."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def fetch_all(self, query, params=()):
        """Получить все записи с параметрами."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
