from backend import db_app
from datetime import datetime
from sqlalchemy.dialects.mysql import TINYINT

class OfficialUser(db_app.Model):

    __tablename__ = 'official_user'

    oid = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    oname = db_app.Column(db_app.String(500), unique=True)
    opsd = db_app.Column(db_app.String(500))
    odate = db_app.Column(db_app.DateTime, default=datetime.utcnow())
    isadmin = db_app.Column(TINYINT)
    imgurl = db_app.Column(db_app.Text())

    def return_json(self):
        dic = {}
        dic['uid'] = self.oid
        dic['username'] = self.oname
        dic['isAdmin'] = self.isadmin
        dic['date'] = self.odate
        dic['password'] = self.opsd
        return dic

    @classmethod
    def get_official_user(cls, args_dic):
        args_list = ['oname', 'oid']
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) != None:
                query_dic[arg] = args_dic.get(arg)

        results = cls.query.filter_by(**query_dic)            

        return [result.return_json() for result in results]


