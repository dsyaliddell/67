import re

class Validator:
    """Валидация пользовательских данных."""

    # Белый список допустимых символов
    LOGIN_PATTERN = re.compile(r'^[A-Za-z0-9]{6,50}$')
    EMAIL_PATTERN = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    PHONE_PATTERN = re.compile(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$')
    FIO_PATTERN = re.compile(r'^[А-Яа-яЁё\s]{2,150}$')

    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """Очистка строки от потенциально опасных символов."""
        if not value:
            return ""
        # Удаление управляющих символов
        cleaned = re.sub(r'[\x00-\x1f\x7f]', '', value)
        # Ограничение длины
        return cleaned[:max_length].strip()

    @staticmethod
    def validate_login(login: str) -> tuple:
        """Логин: латиница и цифры, от 6 до 50 символов."""
        login = Validator.sanitize_string(login, 50)
        if not Validator.LOGIN_PATTERN.match(login):
            return False, "Логин: от 6 до 50 символов, только латиница и цифры"
        return True, ""

    @staticmethod
    def validate_password(password: str) -> tuple:
        """Пароль: минимум 8 символов, максимум 128."""
        if not password or len(password) < 8:
            return False, "Пароль должен содержать минимум 8 символов"
        if len(password) > 128:
            return False, "Пароль слишком длинный (максимум 128 символов)"
        return True, ""

    @staticmethod
    def validate_email(email: str) -> tuple:
        """Email: проверка формата."""
        email = Validator.sanitize_string(email, 100)
        if not Validator.EMAIL_PATTERN.match(email):
            return False, "Некорректный email"
        return True, ""

    @staticmethod
    def validate_phone(phone: str) -> tuple:
        """Телефон: формат 8(XXX)XXX-XX-XX."""
        phone = Validator.sanitize_string(phone, 18)
        if not Validator.PHONE_PATTERN.match(phone):
            return False, "Телефон в формате 8(XXX)XXX-XX-XX"
        return True, ""

    @staticmethod
    def validate_fio(fio: str) -> tuple:
        """ФИО: кириллица и пробелы."""
        fio = Validator.sanitize_string(fio, 150)
        if not Validator.FIO_PATTERN.match(fio):
            return False, "ФИО: только кириллица и пробелы"
        return True, ""

    @staticmethod
    def validate_rating(rating) -> tuple:
        """Оценка: целое число от 1 до 5."""
        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                return True, ""
            return False, "Оценка должна быть от 1 до 5"
        except (ValueError, TypeError):
            return False, "Оценка должна быть числом"
