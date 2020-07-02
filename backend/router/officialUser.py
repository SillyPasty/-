from flask import Blueprint, request, jsonify
from backend import db_app
from backend.models.officalUser import OfficialUser

official_user_bp = Blueprint('official_user', __name__)

@official_user_bp.route('/api/admin', methods=['GET'])
def get_official_user_info():
    args_dic = {}
    username = request.args.get('username', type=str)
    userid = request.args.get('uid', type=int)
    if username != None:
        args_dic['oname'] = username
    if userid != None:
        args_dic['oid'] = userid
    official_users = OfficialUser.get_official_user(args_dic)

    return jsonify({'data': official_users})

@official_user_bp.route('/api/admin', methods=['PUT'])
def put_official_user_info():
    offid = request.args.get('uid', type=int)
    user = OfficialUser().query.filter_by(oid=offid).first()
    if user == None:
        return jsonify({'status': 'fail'})
    else:
        user.oname = request.form.get('username')
        user.isadmin = request.form.get('isAdmin')
        opsd = request.form.get('password')
        if opsd != ' ':
            user.set_password(opsd)
        db_app.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'success'})

@official_user_bp.route('/api/admin', methods=['POST'])
def add_official_user_info():
    user = OfficialUser(
        oname = request.form.get('username'),
        isadmin = request.form.get('isAdmin')
    )
    user.set_password(request.form.get('password'))

    db_app.session.add(user)
    db_app.session.commit()
    return jsonify({'status': 'success'})

@official_user_bp.route('/api/admin', methods=['DELETE'])
def del_official_user_info():
    offid = request.args.get('uid', type=int)
    user = OfficialUser().query.filter_by(oid=offid).first()
    if user == None:
        return jsonify({'status': 'fail'})
    else:
        db_app.session.delete(user)
        db_app.session.commit()
        return jsonify({'status': 'success'})
    