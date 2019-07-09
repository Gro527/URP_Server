from URP_Server.db import db_global,db_stu

def add_course(course_id, course_name, credit):
    if db_global.insert_course(course_id,course_name,credit):
        return True
    return False

def add_class(class_id):
    if db_global.insert_class(class_id):
        return True
    return False

def add_stu(stu_id,name,sex,birthdate,entrance_date,class_id):
    if db_stu.add_stu(stu_id,name,sex,birthdate,entrance_date,class_id):
        return True
    return False

