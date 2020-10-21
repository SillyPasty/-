from backend import db_app
from datetime import datetime
from sqlalchemy.dialects.mysql import TINYINT
from werkzeug.security import generate_password_hash, check_password_hash


class OfficialUser(db_app.Model):

    __tablename__ = 'official_user'

    official_userID = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    oName = db_app.Column(db_app.String(500), unique=True, index=True)
    oPassword = db_app.Column(db_app.String(500))
    oDate = db_app.Column(db_app.DateTime, default=datetime.utcnow())
    isAdmin = db_app.Column(TINYINT)
    imgURL = db_app.Column(db_app.Text())

    def return_json(self):
        dic = {}
        dic['uid'] = self.official_userID
        dic['username'] = self.oName
        dic['isAdmin'] = self.isAdmin
        dic['date'] = self.oDate
        dic['password'] = self.oPassword
        return dic
    
    def set_password(self, password):
        self.oPassword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.oPassword, password)

    @classmethod
    def get_official_user(cls, args_dic):
        args_list = ['oname', 'oid']
        relationship_dic = {
            'oname': 'oName',
            'oid': 'official_userID'
        }
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) != None:
                query_dic[relationship_dic[arg]] = args_dic.get(arg)

        results = cls.query.filter_by(**query_dic)            

        return [result.return_json() for result in results]


