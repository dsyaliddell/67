from flask import Flask, render_template
from backend.routes.auth_routes import auth_bp
from backend.routes.request_routes import request_bp
from backend.routes.admin_routes import admin_bp
from backend.models.user import User

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)
app.secret_key = 'conf2027_secret_key_demo'

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
    app.run(debug=True, host='127.0.0.1', port=5000)
