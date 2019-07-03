from URP_Server.db import db_stu,db_teacher, db_adm

def stu_login(uname,pw):
    try:
        stu = db_stu.get_stu_by_id(uname)
        if stu == None:
            return None
        elif stu["password"] != pw:
            return None
        else:
            del stu["password"]
            return stu
    except:
        return None

def tea_login(uname, pw):
    try:
        tea = db_teacher.get_tea_by_id(uname)
        if tea == None:
            return None
        elif tea['password'] != pw:
            return None
        else:
            del tea['password']
            return tea
    except:
        return None

def adm_login(uname, pw):
    try:
        adm = db_adm.get_adm_by_id(uname)
        if adm == None:
            return None
        elif adm['password'] != pw:
            return None
        else:
            del adm['password']
            return adm
    except:
        return None