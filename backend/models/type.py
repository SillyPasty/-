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
        args_list = ['typeid', 'type1', 'type2', 'typeid_list']
        query_dic = {}
        results = None
        for arg in args_list:
            if args_dic.get(arg) != None:
                if arg == 'typeid_list':
                        results = cls.query.filter(Type.typeid.in_(args_dic[arg]))
                else:            
                    query_dic[arg] = args_dic.get(arg)
        results = results.filter_by(**query_dic) if results else cls.query.filter_by(**query_dic)

        return [result.return_json() for result in results]

