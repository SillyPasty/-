from flask import Blueprint, request, jsonify, Response
from backend import db_app
from backend.models.officalUser import OfficialUser
import json

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def login():
    oname = request.form.get('username')
    opsd = request.form.get('password')

    user = OfficialUser.query.filter_by(oName = oname).first()
    if user != None and user.check_password(opsd):
        result = json.dumps({'status': 'success', 'uid': user.Official_user_official_userID, 'isAdmin': user.isAdmin})
        resp = Response(result, content_type='application/json')
        resp.set_cookie('uid', str(user.Official_user_official_userID))
        resp.set_cookie('isAdmin', str(user.isAdmin))
        return resp
    return jsonify({'status': 'fail'})
