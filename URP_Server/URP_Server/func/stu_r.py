from URP_Server.db import db_stu

def stu_course_info(stu_id):
    return db_stu.get_stu_course_by_stu_id(stu_id)

def stu_info(stu_id):
    return db_stu.get_stu_by_id(stu_id)