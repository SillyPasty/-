from flask import Blueprint, request, jsonify
from backend import db_app
from backend.models.order import Order
from backend.models.detailOrder import DetailOrder


order_bp = Blueprint('order', __name__)

@order_bp.route('/api/order', methods=['GET'])
def get_order_info():
    args_dic = {}
    sellerid = request.args.get('sellerid', type=int)
    orderid = request.args.get('orderid', type=int)
    userid = request.args.get('userid', type=int)
    if sellerid != None:
        args_dic['oid'] = sellerid
    if orderid != None:
        args_dic['orderid'] = orderid
    if userid != None:
        args_dic['uid'] = userid

    return_list = []
    orders = Order.get_order(args_dic)
    if sellerid != None:
        ordid_list = [x['orderid'] for x in orders]
        args_dic['oid_list'] = ordid_list
        return_list = DetailOrder.get_detail_order(args_dic)

    else:
        orderid_list = []
        for order in orders:
            orderid_list.append(order['orderid'])
        detail_orders = DetailOrder.get_detail_order({'oid_list': orderid_list})
        detail_orders_dic = {}
        for detail_order in detail_orders:
            order_id = detail_order.get('order_id')
            if detail_orders_dic.get(order_id) == None:
                detail_orders_dic[order_id] = [detail_order]
            else:
                detail_orders_dic[order_id].append(detail_order)
        for order in orders:
            order['detailorders'] = detail_orders_dic[order['orderid']]
            return_list.append(order)

    return jsonify({'data': return_list})

@order_bp.route('/api/order', methods=['PUT'])
def put_order_info():
    detail_ordid = request.args.get('uid', type=int)
    dorder = DetailOrder().query.filter_by(detailedoid=detail_ordid).first()
    status = request.args.get('status', type=str)
    if dorder == None or status == None:
        return jsonify({'status': 'fail'})
    else:
        dorder.status = status
        db_app.session.commit()
        return jsonify({'status': 'success'})
