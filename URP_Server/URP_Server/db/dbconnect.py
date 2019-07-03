import pymysql
from flask import g
from flask import current_app
from URP_Server import app

a = 'localhost'
uname = 'root'
pw = 'root'
database = 'urp'



def connect_db(a,uname,pw,database):
    db = pymysql.connect(a,uname,pw,database)
    return db

def get_conn():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db(a,uname,pw,database)
    return db

def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        db = None
