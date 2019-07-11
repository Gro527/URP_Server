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


def get_seudent_course_bu_course_id(course_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute(
                "select * from student_course where course_id = '%s'" % (course_id))
            res = cursor.fetchall()
            stu_course_list = []
            for row in res:
                list_item = {}
                list_item['student_id'] = row[0]
                list_item['course_id'] = row[1]
                list_item['score'] = row[2]
                stu_course_list.append(list_item)
            db.commit()
            return stu_course_list
        except:
            db.rollback()
            return []


def get_tea_course_class_by_course_id(course_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            sql = "select t.id,t.name,tcc.class_id from teacher_course_class tcc\
                join teacher t on tcc.teacher_id = t.id\
                     where tcc.course_id = '%s'" % (course_id)
            cursor.execute(sql)
            res = cursor.fetchall()
            tea_course_list = []
            for row in res:
                list_item = {}
                list_item['tea_id'] = row[0]
                list_item['tea_name'] = row[1]
                list_item['class_id'] = row[2]
                tea_course_list.append(list_item)
            db.commit()
            return tea_course_list
        except:
            db.rollback()
            return []


def update_course(course_id, course_name, credit):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("update course set name = '%s', credit = '%s' where id = '%s'" % (
                course_name, credit, course_id))
            db.commit()
            return True
        except:
            db.rollback()
            return False


def delete_course(course_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            sql = "delete from course where id = '%s'" % (
                course_id)
            print(sql)
            cursor.execute(sql)
            db.commit()
            return True
        except:
            db.rollback()
            return False
