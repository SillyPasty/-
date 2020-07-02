from flask import Blueprint, request, jsonify
from backend import db_app
from backend.models.order import Order
from backend.models.detailOrder import DetailOrder
from backend.models.type import Type
from backend.models.product import Product
import datetime


statistic_bp = Blueprint('statistic', __name__)

@statistic_bp.route('/api/statistics/hotproduct', methods=['GET'])
def get_popular_product():
    args_dic = {}
    args_dic['start'] = request.args.get('start')
    args_dic['end'] = request.args.get('end')

    sellerid = request.args.get('sellerid', type=int)
    if sellerid:
        args_dic['oid'] = sellerid

    orders = Order.get_period_order(args_dic)
    args_dic['orderid_list'] = [order['orderid'] for order in orders]

    products = DetailOrder.get_popular_product(args_dic)

    return jsonify({'data': products})

@statistic_bp.route('/api/statistics/seller', methods=['GET'])
def get_seller_sta():
    args_dic = {}
    args_dic['start'] = request.args.get('start')
    args_dic['end'] = request.args.get('end')

    sellerid = request.args.get('sellerid', type=int)
    if sellerid:
        args_dic['oid'] = sellerid

    orders = Order.get_period_order(args_dic)
    args_dic['orderid_list'] = [order['orderid'] for order in orders]

    sellers = DetailOrder.get_seller_sta(args_dic)

    return jsonify({'data': sellers})

@statistic_bp.route('/api/statistics/total', methods=['GET'])
def get_total():
    args_dic = {}
    args_dic['start'] = request.args.get('start')
    args_dic['end'] = request.args.get('end')

    orders = Order.get_period_order(args_dic)
    args_dic['oid_list'] = [order['orderid'] for order in orders]

    detail_orders = DetailOrder.get_detail_order(args_dic)
    totals = 0
    totaln = 0
    for detail_order in detail_orders:
        totals += detail_order['price']
        totaln += detail_order['number']

    return jsonify({'data': {'totalsum': totals, 'totalnumber':totaln}})

@statistic_bp.route('/api/statistics/topseller', methods=['GET'])
def get_topseller():
    args_dic = {}
    args_dic['start'] = request.args.get('start')
    args_dic['end'] = request.args.get('end')

    orders = Order.get_period_order(args_dic)
    args_dic['orderid_list'] = [order['orderid'] for order in orders]

    args_dic['top_flag'] = True
    sellers = DetailOrder.get_seller_sta(args_dic)

    return jsonify({'data': sellers})

@statistic_bp.route('/api/statistics/topuser', methods=['GET'])
def get_topuser():
    args_dic = {}
    args_dic['start'] = request.args.get('start')
    args_dic['end'] = request.args.get('end')

    orders = Order.get_period_order(args_dic)
    args_dic['orderid_list'] = [order['orderid'] for order in orders]

    users = Order.get_user_sta(args_dic)

    return jsonify({'data': users})

@statistic_bp.route('/api/statistics/month', methods=['GET'])
def get_month():
    args_dic = {}
    args_dic['year'] = request.args.get('year', type=int)

    orders_list = Order.get_year_order(args_dic)
    mon_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    result_list = []
    for i, orders in enumerate(orders_list):
        return_dic = {}
        return_dic['month'] = mon_list[i]
        return_dic['ordernumber'] = len(orders)
        return_dic['totalprice'] = 0
        for order in orders:
            return_dic['totalprice'] += order['price']
        result_list.append(return_dic)

    return jsonify({'data': result_list})

@statistic_bp.route('/api/statistics/type', methods=['GET'])
def get_type():
    args_dic = {}
    type1 = request.args.get('type1')
    type2 = request.args.get('type2')
    sellerid = request.args.get('sellerid', type=int)
    if type1: args_dic['type1'] = type1
    if type2: args_dic['type2'] = type2
    if sellerid: args_dic['oid'] = sellerid
    print(args_dic)
    type_list = Type.get_type(args_dic)
    print(len(type_list))
    args_dic['types'] = [types['typeid'] for types in type_list]
    products = Product.get_product(args_dic)
    print(len(products))
    args_dic['pid_list'] = [prod['uid'] for prod in products]
    products = DetailOrder.get_type_product(args_dic)
    print(len(products))
    totals = 0
    totaln = 0
    for product in products:
        totals += product['totalprice']
        totaln += product['totalnumber']


    return jsonify({'data': {'totalsum': totals, 'totalnumber':totaln}})


def timestamp2string(timeStamp):
        d = datetime.datetime.fromtimestamp(timeStamp)
        return d.strftime("%Y-%m-%d")
