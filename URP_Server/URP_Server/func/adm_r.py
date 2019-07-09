from URP_Server.db import db_adm,db_global,db_teacher


def adm_info(adm_id):
    return db_adm.get_adm_by_id(adm_id)

def course_list():
    return db_global.get_course_list()

def course_info(course_id):
    return db_global.get_course_by_id(course_id)

def class_list():
    return db_global.get_class_list()

def class_stu_list(class_id):
    return db_global.get_stu_list_by_class_id(class_id)

def teacher_list():
    return db_teacher.get_tea_list()