from werkzeug.security import generate_password_hash, check_password_hash

# Хеширование
password = "Demo77"
hashed = generate_password_hash(password, method='pbkdf2:sha256:600000', salt_length=16)
print(f"Пароль: {password}")
print(f"Хеш: {hashed}")
print(f"Длина хеша: {len(hashed)}")

# Проверка
print(f"Верный пароль: {check_password_hash(hashed, 'Demo77')}")
print(f"Неверный пароль: {check_password_hash(hashed, 'wrong')}")
