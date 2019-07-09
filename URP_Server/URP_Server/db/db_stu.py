import pymysql
from flask import g
from URP_Server.db import dbconnect
from URP_Server import app
import datetime

def get_stu_by_id(id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("select * from student where id= '%s'" % (id))
            res = cursor.fetchall()[0]
            student = {
                'id' : id,
                'name' : res[1],
                'password' : res[2],
                'sex' : res[3],
                'birthdate' : str(res[4]),
                'entrance_date' : str(res[5]),
                'class_id' : str(res[6])
            }
            db.commit()
            return student
        except IndexError as ie:
            print(ie)
            return None

def get_stu_course_by_stu_id(stu_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            sql = "select c.id, c.name, c.credit, sc.score \
                                from course c \
                                join student_course sc on c.id = sc.course_id\
                                join student s on sc.student_id = s.id\
                                                where s.id = '%s'" % (stu_id)
            cursor.execute(sql)
            res = cursor.fetchall()
            stu_course_list = []
            for row in res:
                list_item = {}
                list_item['course_id'] = row[0]
                list_item['course_name'] = row[1]
                list_item['credit'] = row[2]
                list_item['score'] = row[3]
                stu_course_list.append(list_item)
            db.commit()
            return stu_course_list
        except IndexError as ie:
            print(ie)
            return []

def add_stu(stu_id,name,sex,birthdate,entrance_date,class_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            sql = "insert into student(id,password,name,sex,birthdate,entrance_date,class_id) values(\
                '%s','%s','%s',%s,'%s','%s','%s')" % (stu_id,stu_id,name,sex,birthdate,entrance_date,class_id)
            print(sql)
            cursor.execute(sql)
            db.commit()
            return True
        except:
            db.rollback()
            return False