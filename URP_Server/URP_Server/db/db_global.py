import pymysql
from flask import g
from URP_Server.db import dbconnect
from URP_Server import app


def get_course_by_id(course_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("select * from course where id= '%s'" % (course_id))
            res = cursor.fetchall()[0]
            course = {
                'id': course_id,
                'name': res[1],
                'credit': res[2],
            }
            return course
        except IndexError as ie:
            print(ie)
            return None


def get_course_list():
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("select id,name from course")
            res = cursor.fetchall()
            course_list = []
            for row in res:
                course = {}
                course['id'] = row[0]
                course['name'] = row[1]
                course_list.append(course)
            return course_list
        except IndexError as ie:
            print(ie)
            return None


def insert_course(course_id, course_name, credit):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("insert into course(id,name,credit) values('%s','%s',%s)" % (
                course_id, course_name, credit))
            db.commit()
            return True
        except:
            db.rollback()
            return False


def get_class_list():
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("select * from class")
            res = cursor.fetchall()
            class_list = []
            for row in res:
                cl = {}
                cl['id'] = row[0]
                class_list.append(cl)
            db.commit()
            return class_list
        except:
            db.rollback()
            return None


def get_stu_list_by_class_id(class_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute(
                "select * from student where class_id = '%s'" % (class_id))
            res = cursor.fetchall()
            student_list = []
            for row in res:
                stu = {
                    'id': row[0],
                    'name': row[1],
                    'sex': row[3],
                    'birthdate': str(row[4]),
                    'entrance_date': str(row[5]),
                    'class_id': str(row[6])
                }
                student_list.append(stu)
            return student_list
        except IndexError as ie:
            print(ie)
            return None
        except:
            db.rollback()
            return None

def insert_class(class_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("insert into class(id) values('%s')" % (class_id))
            db.commit()
            return True
        except:
            db.rollback()
            return False