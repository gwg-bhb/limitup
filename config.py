#encoding: utf-8
import os
from sqlalchemy import create_engine

DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '123.57.81.203'
PORT     = '3306'
DATABASE = 'limit_up'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


mysql_engine = create_engine(DB_URI)

SQLALCHEMY_TRACK_MODIFICATIONS = False