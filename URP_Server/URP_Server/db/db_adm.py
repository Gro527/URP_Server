import pymysql
from flask import g
from URP_Server.db import dbconnect
from URP_Server import app
import datetime

def get_adm_by_id(id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("select * from admin where id= '%s'" % (id))
            res = cursor.fetchall()[0]
            admin = {
                'id' : id,
                'name' : res[1],
                'password' : res[2],
            }
            return admin
        except IndexError as ie:
            print(ie)
            return None