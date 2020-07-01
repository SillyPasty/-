

import os

class FlaskConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    HOSTNAME = 'cdb-iien6iby.cd.tencentcdb.com'
    PORT = '10115'
    DATABASE = 'firm_infos'
    USERNAME = 'root'
    PASSWORD = 'semester07'
    DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
