from flask import session

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.authenticate(
        data.get('login', ''),
        data.get('password', '')
    )
    if not user:
        return jsonify({
            'success': False,
            'message': 'Неверный логин или пароль'
        }), 401

    # Очистка старой сессии (защита от fixation)
    session.clear()

    # Создание новой сессии
    session['user_id'] = user['id']
    session['role'] = user['role']
    session['login'] = user['login']

    # Сессия постоянная (с ограниченным временем жизни)
    session.permanent = True

    return jsonify({
        'success': True,
        'role': user['role'],
        'redirect': '/admin' if user['role'] == 'admin' else '/dashboard'
    }), 200
