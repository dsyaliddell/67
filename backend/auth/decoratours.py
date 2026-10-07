from flask import request
from functools import wraps
from flask import session, jsonify, redirect, url_for


def login_required(f):
    """Декоратор: требует авторизации."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Для API-запросов — JSON-ответ
            if request.path.startswith('/api/'):
                return jsonify({
                    'success': False,
                    'message': 'Требуется авторизация'
                }), 401
            # Для страниц — редирект на логин
            return redirect('/api/auth/login')
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Декоратор: требует прав администратора."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'message': 'Требуется авторизация'
            }), 401
        if session.get('role') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Доступ запрещён. Требуются права администратора'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


def participant_required(f):
    """Декоратор: требует роли участника (user) или администратора."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'message': 'Требуется авторизация'
            }), 401
        if session.get('role') not in ('user', 'admin'):
            return jsonify({
                'success': False,
                'message': 'Доступ запрещён. Требуется роль участника'
            }), 403
        return f(*args, **kwargs)
    return decorated_function
