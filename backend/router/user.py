from flask import Blueprint, request, jsonify
from backend import db_app
from backend.models.user import User
from backend.models.cart import Cart
import random
import string

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/user', methods=['GET'])
def get_user_info():
    args_dic = {}
    username = request.args.get('username', type=str)
    if username != None:
        args_dic['username'] = username
    official_users = User.get_user(args_dic)

    return jsonify({'data': official_users})

@user_bp.route('/api/user', methods=['PUT'])
def put_user_info():
    offid = request.args.get('uid', type=int)
    user = User().query.filter_by(uid=offid).first()
    if user == None:
        return jsonify({'status': 'fail'})
    else:
        user.username = request.form.get('username')
        user.gender = request.form.get('gender')
        user.userpsd = request.form.get('password')
        user.address = request.form.get('address')
        user.phone = request.form.get('tel')
        db_app.session.commit()
        return jsonify({'status': 'success'})

@user_bp.route('/api/user', methods=['POST'])
def add_user_info():
    user = User(
        username = request.form.get('username'),
        gender = request.form.get('gender'),
        userpsd = request.form.get('password'),
        address = request.form.get('address'),
        phone = request.form.get('tel')
    )
    db_app.session.add(user)
    db_app.session.commit()
    return jsonify({'status': 'success'})

@user_bp.route('/api/user', methods=['DELETE'])
def del_user_info():
    usrid = request.args.get('uid', type=int)
    user = User().query.filter_by(uid=usrid).first()
    if user == None:
        return jsonify({'status': 'fail'})
    else:
        db_app.session.delete(user)
        db_app.session.commit()
        return jsonify({'status': 'success'})

@user_bp.route('/api/user/psw', methods=['PUT'])
def reset_user_psw():
    offid = request.args.get('uid', type=int)
    user = User().query.filter_by(uid=offid).first()
    if user == None:
        return jsonify({'status': 'fail'})
    else:
        new_psd = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        user.userpsd = salt = new_psd
        db_app.session.commit()
        return jsonify({'status': 'success', 'newpsw': new_psd})