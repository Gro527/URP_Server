import pymysql
from flask import g
from URP_Server.db import dbconnect
from URP_Server import app
import datetime

def get_tea_by_id(id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("select * from teacher where id= '%s'" % (id))
            res = cursor.fetchall()[0]
            teacher = {
                'id' : id,
                'name' : res[1],
                'password' : res[2],
                'course_list':[]
            }
            cursor.execute("select tcc.course_id,c.name,tcc.class_id from teacher_course_class tcc join course c on tcc.course_id = c.id where teacher_id = '%s'" % (id))
            res = cursor.fetchall()
            for row in res:
                tc ={
                    'course_id':row[0],
                    'course_name':row[1],
                    'class_id':row[2]
                }
                teacher['course_list'].append(tc)
            db.commit()
            return teacher
        except IndexError as ie:
            print(ie)
            return None

def get_class_stu_course(teacher_id, class_id, course_id):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor= db.cursor()
            sql = "select s.id,s.name,sc.score from student s \
                                join student_course sc on s.id = sc.student_id \
                                join course c on c.id = sc.course_id \
                                join teacher_course_class tcc on c.id = tcc.course_id \
                                join class cl on cl.id = tcc.class_id    \
                                where tcc.teacher_id = '%s' and tcc.course_id = '%s' \
                                        and tcc.class_id = '%s' and s.class_id = cl.id" % (teacher_id,course_id,class_id)
            cursor.execute(sql)
            res = cursor.fetchall()
            class_course_list = []
            for row in res:
                stu_course = {}
                stu_course['student_id'] = row[0]
                stu_course['student_name'] = row[1]
                stu_course['score'] = row[2]
                class_course_list.append(stu_course)
            db.commit()
            return class_course_list
        except IndexError as ie:
            print(ie)
            return None

def set_score(stu_id,course_id,score):
    with app.app_context():
        try:
            db = dbconnect.get_conn()
            cursor = db.cursor()
            cursor.execute("update student_course set score = %s where student_id = '%s' and course_id = '%s'" % (score,stu_id,course_id))
            db.commit()
        except:
            return False
        return True