from backend import db_app
from datetime import datetime

class Type(db_app.Model):

    __tablename__ = 'type'

    typeid = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    type1 = db_app.Column(db_app.String(500), unique=False)
    type2 = db_app.Column(db_app.String(500), unique=True)

    def return_json(self):
        dic = {}
        dic['type1'] = self.type1
        dic['type2'] = self.type2
        dic['typeid'] = self.typeid
        return dic
    
    @classmethod
    def get_type(cls, args_dic):
        args_list = ['typeid', 'type1', 'type2']
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) != None:
                query_dic[arg] = args_dic.get(arg)
        results = cls.query.filter_by(**query_dic)            

        return [result.return_json() for result in results]

