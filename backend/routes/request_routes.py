from flask import Blueprint, request, jsonify, render_template, session
from backend.models.request import Request
from backend.models.event import Event

request_bp = Blueprint('requests', __name__)


def _check_auth():
    if 'user_id' not in session:
        return False
    return True


@request_bp.route('/dashboard')
def dashboard():
    if not _check_auth():
        return render_template('login.html')
    return render_template('dashboard.html')


@request_bp.route('/api/requests', methods=['GET'])
def get_my_requests():
    if not _check_auth():
        return jsonify({'success': False, 'message': 'Не авторизован'}), 401
    data = Request.get_by_user(session['user_id'])
    return jsonify({'success': True, 'requests': data}), 200


@request_bp.route('/create_request', methods=['GET', 'POST'])
def create_request():
    if not _check_auth():
        return render_template('login.html')

    if request.method == 'GET':
        events = Event.get_all()
        return render_template('create_request.html', events=events)

    data = request.get_json()
    new_request = Request(
        user_id=session['user_id'],
        event_id=int(data.get('event_id')),
        status_id=1  # «Новая»
    )
    request_id = new_request.save()
    return jsonify({'success': True, 'request_id': request_id}), 201
