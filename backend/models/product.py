from backend import db_app
from datetime import datetime
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

class Product(db_app.Model):

    __tablename__ = 'product'

    itemID = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    iName = db_app.Column(db_app.String(500))
    iPrice = db_app.Column(DOUBLE)
    iDate = db_app.Column(db_app.DateTime, default=datetime.utcnow())
    remain = db_app.Column(db_app.Integer)
    description = db_app.Column(db_app.String(500))

    Official_user_official_userID = db_app.Column(db_app.Integer, db_app.ForeignKey('official_user.official_userID'), index=True)
    Type_typeID = db_app.Column(db_app.Integer, db_app.ForeignKey('type.typeID'), index=True)
    type = relationship('Type', backref='product_type')

    def return_json(self):
        dic = {}
        dic['uid'] = self.itemID
        dic['sellerid'] = self.Official_user_official_userID
        dic['productname'] = self.iName
        dic['price'] = (float)(self.iPrice)
        dic['date'] = self.iDate
        dic['description'] = self.description
        dic['remain'] = self.remain
        dic['typeid'] = self.Type_typeID
        
        return dic
    
    @classmethod
    def get_product(cls, args_dic):
        args_list = ['oid', 'pname', 'types', 'pid']
        relation_dic = {
            'oid': 'Official_user_official_userID',
            'pname': 'iName',
            'pid': 'itemID'
        }
        query_dic = {}
        results = None
        for arg in args_list:
            if args_dic.get(arg) != None:
                if arg == 'types':
                    results = cls.query.filter(Product.Type_typeID.in_(args_dic[arg]))
                else:
                    query_dic[relation_dic[arg]] = args_dic.get(arg)
        
        results = results.filter_by(**query_dic) if results else cls.query.filter_by(**query_dic)

        return [result.return_json() for result in results]

