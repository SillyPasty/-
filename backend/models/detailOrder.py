from backend import db_app
from datetime import datetime
from sqlalchemy.dialects.mysql import TINYINT, DOUBLE
from sqlalchemy.orm import relationship
from sqlalchemy import func
from backend.models.product import Product
from backend.models.officalUser import OfficialUser

class DetailOrder(db_app.Model):

    __tablename__ = 'detailed_order'

    detailed_orderID = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    iNumber = db_app.Column(db_app.Integer)
    dPrice = db_app.Column(DOUBLE)
    status = db_app.Column(db_app.String(50))

    Order_orderID = db_app.Column(db_app.Integer, db_app.ForeignKey('all_order.orderID'), index=True)
    order = relationship('Order', backref='detail_of_order')

    Product_itemID = db_app.Column(db_app.Integer, db_app.ForeignKey('product.itemID'), index=True)
    product = relationship('Product', backref='product_detailorder')

    Official_user_official_userID = db_app.Column(db_app.Integer, db_app.ForeignKey('official_user.official_userID'), index=True)
    official_user = relationship('OfficialUser', backref='official_detailorder')

    def return_json(self):
        dic = {}

        dic['detailorderid'] = self.detailed_orderID
        dic['sellerid'] = self.Official_user_official_userID
        dic['productid'] = self.Product_itemID
        dic['price'] = (float)(self.dPrice)
        dic['number'] = self.iNumber
        dic['status'] = self.status
        dic['order_id'] = self.Order_orderID
        return dic
    
    @classmethod
    def get_detail_order(cls, args_dic):
        args_list = ['detailedoid', 'orderid', 'oid', 'pid', 'status', 'oid_list']
        relationship_dic = {
            'detailedoid': 'detailed_orderID',
            'orderid': 'Order_orderID',
            'oid': 'Official_user_official_userID',
            'pid': 'Product_itemID',
            'status': 'status',
        }
        query_dic = {}
        results = None
        for arg in args_list:
            if args_dic.get(arg) != None:
                if arg == 'oid_list':
                    results = cls.query.filter(DetailOrder.Order_orderID.in_(args_dic[arg]))
                else:
                    query_dic[relationship_dic[arg]] = args_dic.get(arg)

        results = results.filter_by(**query_dic) if results else cls.query.filter_by(**query_dic)

        return [result.return_json() for result in results]
    
    @classmethod
    def get_popular_product(cls, args_dic):
        args_list = ['oid']
        relationship_dic = {
            'detailedoid': 'detailed_orderID',
            'orderid': 'Order_orderID',
            'oid': 'Official_user_official_userID',
            'pid': 'Product_itemID',
            'status': 'status',
        }
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) != None:
                    query_dic[relationship_dic[arg]] = args_dic.get(arg)

        results = db_app.session().query(cls.Product_itemID,
                                         func.sum(cls.dPrice).label('sums'),
                                         func.sum(cls.iNumber).label('numbers')). \
                                            group_by(cls.Product_itemID). \
                                            filter(cls.Order_orderID.in_(args_dic['orderid_list'])).\
                                            filter(cls.status != 'canceled').\
                                            filter_by(**query_dic).\
                                            order_by(db_app.desc('sums'))

        result_list = []
        for i, res in enumerate(results.all()):
            if i >= 10: break
            args_dic['pid'] = res[0]
            prod = Product.get_product(args_dic)[0]
            prod['totalprice'] = (float)(res[1])
            prod['totalnumber'] = (float)(res[2])
            result_list.append(prod)
        
        return result_list
    
    @classmethod
    def get_seller_sta(cls, args_dic):
        args_list = ['oid']
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) != None:
                    query_dic['Official_user_official_userID'] = args_dic.get(arg)

        results = db_app.session().query(cls.Official_user_official_userID,
                                         func.sum(cls.dPrice).label('sums'),
                                         func.sum(cls.iNumber).label('numbers')). \
                                            group_by(cls.Official_user_official_userID). \
                                            filter(cls.Order_orderID.in_(args_dic['orderid_list'])).\
                                            filter(cls.status != 'canceled').\
                                            filter_by(**query_dic).\
                                            order_by(db_app.desc('sums'))

        result_list = []
        for i, res in enumerate(results.all()):
            if i >= 10 and args_dic.get('top_flag'): break
            args_dic['oid'] = res[0]
            seller = OfficialUser.get_official_user(args_dic)[0]
            seller['totalprice'] = (float)(res[1])
            seller['totalnumber'] = (float)(res[2])
            result_list.append(seller)
        
        return result_list

    @classmethod
    def get_type_product(cls, args_dic):
        args_list = ['oid']
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) != None:
                    query_dic['Official_user_official_userID'] = args_dic.get(arg)

        results = db_app.session().query(cls.Product_itemID,
                                         func.sum(cls.dPrice).label('sums'),
                                         func.sum(cls.iNumber).label('numbers')). \
                                            group_by(cls.Product_itemID). \
                                            filter(cls.Product_itemID.in_(args_dic['pid_list'])).\
                                            filter(cls.status != 'canceled').\
                                            filter_by(**query_dic).\
                                            order_by(db_app.desc('sums'))

        result_list = []
        for i, res in enumerate(results.all()):
            args_dic['pid'] = res[0]
            prod = Product.get_product(args_dic)[0]
            prod['totalprice'] = (float)(res[1])
            prod['totalnumber'] = (float)(res[2])
            result_list.append(prod)
        
        return result_list