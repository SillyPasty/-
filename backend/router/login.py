from flask import Blueprint, request, jsonify, Response
from backend import db_app
from backend.models.officalUser import OfficialUser
import json

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def login():
    oname = request.form.get('username')
    opsd = request.form.get('password')

    args_dic = {}
    if oname != None:
        args_dic['oname'] = oname
    user = OfficialUser.get_official_user(args_dic)[0]
    if user['password'] == opsd:
        result = json.dumps({'status': 'success', 'uid': user['uid'], 'isAdmin': user['isAdmin']})
        resp = Response(result, content_type='application/json')
        resp.set_cookie('uid', str(user['uid']))
        resp.set_cookie('isAdmin', str(user['isAdmin']))
        return resp
    return jsonify({'status': 'fail'})
