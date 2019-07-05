from URP_Server.db import db_teacher

def tea_info(tea_id):
    return db_teacher.get_tea_by_id(tea_id)

def tea_class_course(tea_id, class_id, course_id):
    return db_teacher.get_class_stu_course(tea_id,class_id,course_id)