from backend.database import Database

class BaseModel:
    """Базовый класс для всех моделей. Демонстрирует наследование."""
    table_name = None

    def __init__(self, **kwargs):
        self.db = Database()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """Метод должен быть переопределён в дочерних классах."""
        raise NotImplementedError("Метод save() должен быть реализован")

    @classmethod
    def get_all(cls):
        db = Database()
        return db.fetch_all(f"SELECT * FROM {cls.table_name}")

    @classmethod
    def get_by_id(cls, record_id: int):
        db = Database()
        return db.fetch_one(
            f"SELECT * FROM {cls.table_name} WHERE id = ?",
            (record_id,)
        )
