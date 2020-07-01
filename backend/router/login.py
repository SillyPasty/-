from flask import Blueprint, request, jsonify, Response
from backend import db_app
from backend.models.officalUser import OfficialUser
import json

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def login():
    oname = request.form.get('username')
    opsd = request.form.get('password')

    user = OfficialUser.query.filter_by(oname = oname).first()
    if user.check_password(opsd):
        result = json.dumps({'status': 'success', 'uid': user.oid, 'isAdmin': user.isadmin})
        resp = Response(result, content_type='application/json')
        resp.set_cookie('uid', str(user.oid))
        resp.set_cookie('isAdmin', str(user.isadmin))
        return resp
    return jsonify({'status': 'fail'})
