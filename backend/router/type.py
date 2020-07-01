from flask import Blueprint, request, jsonify
from backend import db_app
from backend.models.type import Type


type_bp = Blueprint('type', __name__)

@type_bp.route('/api/type', methods=['GET'])
def get_type():
    args_dic = {}
    f_type = request.args.get('first_type', type=str)
    if f_type != None:
        args_dic['type1'] = f_type
    types = Type.get_type(args_dic)
    dic = {}
    for t in types:
        item = {
            'secondtypename': t['type2'],
            'typeid': t['typeid']
        }
        if dic.get(t['type1']) == None:
            dic[t['type1']] = [item]
        else:
            dic[t['type1']].append(item)
    result = []
    for k, v in dic.items():
        result.append({
            'firsttypename': k,
            'secondtype': v
        })
    return jsonify({'data': result})

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