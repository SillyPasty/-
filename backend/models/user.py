from backend import db_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db_app.Model):

    __tablename__ = 'user'

    userID = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    uName = db_app.Column(db_app.String(500), unique=True)
    uPassword = db_app.Column(db_app.String(500))
    uDate = db_app.Column(db_app.DateTime, default=datetime.utcnow())
    gender = db_app.Column(db_app.String(5))
    tel = db_app.Column(db_app.String(500))
    address = db_app.Column(db_app.String(500))
    imgURL = db_app.Column(db_app.Text())


    def return_json(self):
        dic = {'uid': self.userID, 'username': self.uName, 'gender': self.gender, 'tel': self.tel,
               'address': self.address, 'date': self.uDate, 'password': self.uPassword}

        return dic
    
    @classmethod
    def get_user(cls, args_dic):
        relation_dic = {
            'uid': 'userID',
            'username': 'uName',
        }
        args_list = ['username', 'uid']
        query_dic = {}
        for arg in args_list:
            if args_dic.get(arg) is not None:
                query_dic[relation_dic[arg]] = args_dic.get(arg)

        results = cls.query.filter_by(**query_dic)            

        return [result.return_json() for result in results]
    
    def set_password(self, password):
        self.uPassword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.uPassword, password)

