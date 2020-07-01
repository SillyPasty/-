from backend import db_app
from datetime import datetime

class User(db_app.Model):

    __tablename__ = 'user'

    uid = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    username = db_app.Column(db_app.String(500), unique=True)
    userpsd = db_app.Column(db_app.String(500))
    date = db_app.Column(db_app.DateTime, default=datetime.utcnow())
    gender = db_app.Column(db_app.String(5))
    phone = db_app.Column(db_app.String(500))
    address = db_app.Column(db_app.String(500))
    imgurl = db_app.Column(db_app.Text())

    def return_json(self):
        dic = {}
        dic['uid'] = self.uid
        dic['username'] = self.username
        dic['gender'] = self.gender
        dic['tel'] = self.phone
        dic['address'] = self.address
        dic['date'] = self.date
        dic['password'] = self.userpsd

        return dic
    
    @classmethod
    def get_user(cls, args_dic):
        args_list = ['username', 'uid']
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) != None:
                query_dic[arg] = args_dic.get(arg)

        results = cls.query.filter_by(**query_dic)            

        return [result.return_json() for result in results]

