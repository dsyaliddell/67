from backend.models.base_model import BaseModel
from backend.validators.validators import Validator
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    table_name = "user"

    def __init__(self, login=None, password=None, email=None,
                 phone=None, role='user', **kwargs):
        super().__init__(**kwargs)
        self.login = login
        self.password = password
        self.email = email
        self.phone = phone
        self.role = role

    def validate(self) -> tuple:
        """Полная валидация полей пользователя."""
        checks = [
            Validator.validate_login(self.login),
            Validator.validate_password(self.password),
            Validator.validate_email(self.email),
            Validator.validate_phone(self.phone),
        ]
        for ok, msg in checks:
            if not ok:
                return False, msg
        return True, ""

    def login_exists(self) -> bool:
        """Проверка уникальности логина."""
        row = self.db.fetch_one(
            "SELECT id FROM user WHERE login = ?", (self.login,)
        )
        return row is not None

    def email_exists(self) -> bool:
        row = self.db.fetch_one(
            "SELECT id FROM user WHERE email = ?", (self.email,)
        )
        return row is not None

    def save(self) -> tuple:
        """Сохранение нового пользователя с валидацией."""
        ok, msg = self.validate()
        if not ok:
            return False, msg
        if self.login_exists():
            return False, "Пользователь с таким логином уже существует"
        if self.email_exists():
            return False, "Пользователь с таким email уже существует"

        password_hash = generate_password_hash(self.password)
        user_id = self.db.execute(
            """INSERT INTO user (login, password_hash, email, phone, role)
               VALUES (?, ?, ?, ?, ?)""",
            (self.login, password_hash, self.email, self.phone, self.role)
        )
        self.id = user_id
        return True, user_id

    @staticmethod
    def authenticate(login: str, password: str) -> dict:
        """Аутентификация по логину и паролю."""
        db = Database()
        user = db.fetch_one("SELECT * FROM user WHERE login = ?", (login,))
        if user and check_password_hash(user['password_hash'], password):
            return user
        return None
