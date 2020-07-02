from flask import Blueprint, request, jsonify
from backend import db_app
from backend.models.type import Type


type_bp = Blueprint('type', __name__)

@type_bp.route('/api/type', methods=['GET'])
def get_type():
    args_dic = {}
    f_type = request.args.get('first_type')
    if f_type != None:
        args_dic['type1'] = f_type
    types = Type.get_type(args_dic)
    
    return jsonify({'data': types})

@type_bp.route('/api/type', methods=['POST'])
def add_type():
    typ = Type(
        type1 = request.form.get('firsttype'),
        type2 = request.form.get('secondtype')
    )
    db_app.session.add(typ)
    db_app.session.commit()
    return jsonify({'status': 'success'})

@type_bp.route('/api/type', methods=['DELETE'])
def del_type():
    tid = request.args.get('typeid', type=int)
    typ = Type().query.filter_by(typeid=tid).first()
    if typ == None:
        return jsonify({'status': 'fail'})
    else:
        db_app.session.delete(typ)
        db_app.session.commit()
        return jsonify({'status': 'success'})