from backend.database import Database

db = Database()

# Попытка SQL-инъекции
malicious_login = "' OR '1'='1"
result = db.fetch_all(
    "SELECT * FROM user WHERE login = ?",
    (malicious_login,)
)
print(f"Результат инъекции: {len(result)} записей")
# Ожидается: 0 записей (инъекция не сработала)
