from URP_Server.db import db_teacher

def up_score(stu_id,course_id,score):
    return db_teacher.set_score(stu_id,course_id,score)