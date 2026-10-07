from flask import Blueprint, request, jsonify, render_template, session
from backend.models.request import Request

admin_bp = Blueprint('admin', __name__)


def _check_admin():
    return session.get('role') == 'admin'


@admin_bp.route('/admin')
def admin_panel():
    if not _check_admin():
        return render_template('login.html')
    return render_template('admin.html')


@admin_bp.route('/api/admin/requests', methods=['GET'])
def get_all_requests():
    if not _check_admin():
        return jsonify({'success': False, 'message': 'Доступ запрещён'}), 403
    data = Request.get_all_with_details()
    return jsonify({'success': True, 'requests': data}), 200


@admin_bp.route('/api/admin/requests/<int:request_id>', methods=['PUT'])
def update_request_status(request_id):
    if not _check_admin():
        return jsonify({'success': False, 'message': 'Доступ запрещён'}), 403
    data = request.get_json()
    status_id = int(data.get('status_id'))
    if status_id not in (1, 2, 3):
        return jsonify({'success': False, 'message': 'Некорректный статус'}), 400
    Request.update_status(request_id, status_id)
    return jsonify({'success': True}), 200
