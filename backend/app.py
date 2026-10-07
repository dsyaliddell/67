import os
from flask import Flask

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

# ═══════════════════════════════════════════════════════════
# БЕЗОПАСНАЯ НАСТРОЙКА СЕССИЙ И COOKIES
# ═══════════════════════════════════════════════════════════

# Секретный ключ: длинный, случайный, из переменной окружения
app.secret_key = os.environ.get(
    'FLASK_SECRET_KEY',
    'dev-fallback-key-change-in-production-32bytes-min'
)

# Флаги безопасности cookies
app.config.update(
    # Только HTTPS (в разработке False, в продакшене True)
    SESSION_COOKIE_SECURE=False,  # Для production: True

    # Запрет доступа из JavaScript (защита от XSS)
    SESSION_COOKIE_HTTPONLY=True,

    # Защита от CSRF: cookies не отправляются при cross-site запросах
    SESSION_COOKIE_SAMESITE='Lax',

    # Время жизни сессии: 30 минут
    PERMANENT_SESSION_LIFETIME=1800,

    # Имя cookie
    SESSION_COOKIE_NAME='conf_session',
)

# ═══════════════════════════════════════════════════════════
# РЕГИСТРАЦИЯ BLUEPRINTS
# ═══════════════════════════════════════════════════════════

from backend.routes.auth_routes import auth_bp
from backend.routes.request_routes import request_bp
from backend.routes.admin_routes import admin_bp
from backend.models.user import User

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(request_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def index():
    return render_template('login.html')


def init_admin():
    """Создание администратора по умолчанию."""
    admin = User(
        login='Conf2027',
        password='Demo77',
        email='admin@conf2027.ru',
        phone='8(999)000-00-00',
        role='admin'
    )
    if not admin.login_exists():
        admin.save()
        print("✓ Администратор Conf2027 создан")


if __name__ == '__main__':
    init_admin()
    app.run(debug=False, host='127.0.0.1', port=5000)
