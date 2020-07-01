from backend import db_app
from datetime import datetime
from sqlalchemy.dialects.mysql import DOUBLE

class Cart(db_app.Model):

    __tablename__ = 'cart'

    cid = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    cnumber = db_app.Column(db_app.Integer)
    cprice = db_app.Column(DOUBLE)

    pid = db_app.Column(db_app.Integer, db_app.ForeignKey('product.pid'))
    uid = db_app.Column(db_app.Integer, db_app.ForeignKey('user.uid'))

    def return_json(self):
        dic = {}

