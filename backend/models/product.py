from backend import db_app
from datetime import datetime
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

class Product(db_app.Model):

    __tablename__ = 'product'

    pid = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    pname = db_app.Column(db_app.String(500))
    pprice = db_app.Column(DOUBLE)
    pdate = db_app.Column(db_app.DateTime, default=datetime.utcnow())
    remain = db_app.Column(db_app.Integer)
    description = db_app.Column(db_app.String(500))

    oid = db_app.Column(db_app.Integer, db_app.ForeignKey('official_user.oid'))
    typeid = db_app.Column(db_app.Integer, db_app.ForeignKey('type.typeid'))
    type = relationship('Type', backref='product_type')

    def return_json(self):
        dic = {}
        dic['uid'] = self.pid
        dic['sellerid'] = self.oid
        dic['productname'] = self.pname
        dic['price'] = (float)(self.pprice)
        dic['date'] = self.pdate
        dic['description'] = self.description
        dic['remain'] = self.remain
        dic['typeid'] = self.typeid
        
        return dic
    
    @classmethod
    def get_product(cls, args_dic):
        args_list = ['oid', 'pname', 'types', 'pid']
        query_dic = {}
        results = None
        for arg in args_list:
            if args_dic.get(arg) != None:
                if arg == 'types':
                    results = cls.query.filter(Product.typeid.in_(args_dic[arg]))
                else:
                    query_dic[arg] = args_dic.get(arg)
        
        results = results.filter_by(**query_dic) if results else cls.query.filter_by(**query_dic)

        return [result.return_json() for result in results]

