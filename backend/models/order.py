from backend import db_app
from backend.models.detailOrder import DetailOrder
from backend.models.user import User
from datetime import datetime
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship
from sqlalchemy import func


class Order(db_app.Model):
    __tablename__ = 'all_order'

    orderID = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    oPrice = db_app.Column(DOUBLE)
    oDate = db_app.Column(db_app.DateTime, default=datetime.utcnow())
    address = db_app.Column(db_app.String(500))

    User_userID = db_app.Column(db_app.Integer, db_app.ForeignKey('user.userID'), index=True)
    user = relationship('User', backref='order_of_user')

    def return_json(self):
        dic = {}
        dic['orderid'] = self.orderID
        dic['price'] = (float)(self.oPrice)
        dic['address'] = self.address
        dic['date'] = self.oDate
        dic['userid'] = self.User_userID
        return dic

    @classmethod
    def get_order(cls, args_dic):
        args_list = ['orderid', 'uid']
        relation_dic = {
            'orderid': 'orderID',
            'uid': 'User_userID'
        }
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) != None:
                query_dic[relation_dic[arg]] = args_dic.get(arg)

        results = cls.query.filter_by(**query_dic)

        return [result.return_json() for result in results]

    @classmethod
    def get_period_order(cls, args_dic):
        st = datetime.strptime(args_dic['start'], '%Y-%m-%d')
        et = datetime.strptime(args_dic['end'], '%Y-%m-%d')
        results = cls.query.filter(cls.oDate >= st).filter(cls.oDate < et)

        return [result.return_json() for result in results]

    @classmethod
    def get_year_order(cls, args_dic):
        year = args_dic['year']
        result_list = []
        for i in range(12):
            st = datetime.strptime('{:d}-{:d}'.format(year, i + 1), '%Y-%m')
            et = None
            if i == 11:
                et = datetime.strptime('{:d}-{:d}'.format(year + 1, 1), '%Y-%m')
            else:
                et = datetime.strptime('{:d}-{:d}'.format(year, i + 2), '%Y-%m')

            results = cls.query.filter(cls.oDate >= st).filter(cls.oDate < et)
            result_list.append([result.return_json() for result in results])

        return result_list

    @classmethod
    def get_user_sta(cls, args_dic):

        results = db_app.session().query(cls.User_userID, func.sum(cls.oPrice).label('sums')). \
            group_by(cls.User_userID). \
            filter(cls.orderID.in_(args_dic['orderid_list'])). \
            order_by(db_app.desc('sums'))

        result_list = []
        for i, res in enumerate(results.all()):
            if i >= 10: break
            args_dic['uid'] = res[0]
            user = User.get_user(args_dic)[0]
            user['totalprice'] = (float)(res[1])
            result_list.append(user)

        return result_list
