from URP_Server.db import db_global,db_stu,db_teacher

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

def mod_course(course_id, course_name, credit):
    if db_global.update_course(course_id, course_name, credit):
        return True
    return False

def del_course(course_id):
    if db_global.delete_course(course_id):
        return True
    return False

def del_stu(stu_id):
    if db_global.delete_student(stu_id):
        return True
    return False

def del_class(class_id):
    if db_global.delete_class(class_id):
        return True
    return False

def mod_stu(stu_id,name,sex,birthdate,entrance_date,class_id):
    if db_stu.update_stu(stu_id,name,sex,birthdate,entrance_date,class_id):
        return True
    return False

def add_tea(teacher_id, name):
    if db_teacher.insert_teacher(teacher_id,name):
        return True
    return False

def mod_tea(teacher_id, name):
    if db_teacher.update_teacher(teacher_id,name):
        return True
    return False

def del_teacher(teacher_id):
    if db_teacher.delete_teacher(teacher_id):
        return True
    return False