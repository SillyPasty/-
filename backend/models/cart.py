from backend import db_app
from datetime import datetime
from sqlalchemy.dialects.mysql import DOUBLE

class Cart(db_app.Model):

    __tablename__ = 'cart'

    cartID = db_app.Column(db_app.Integer, primary_key=True, autoincrement=True, index=True)
    cNumber = db_app.Column(db_app.Integer)
    cPrice = db_app.Column(DOUBLE)

    Product_itemID = db_app.Column(db_app.Integer, db_app.ForeignKey('product.itemID'), index=True)
    User_userID = db_app.Column(db_app.Integer, db_app.ForeignKey('user.userID'), index=True)

    def return_json(self):
        dic = {}

