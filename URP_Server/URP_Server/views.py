"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from URP_Server import app
from URP_Server.db import db_stu
from URP_Server import func
import json


# pages
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'login.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/test')
def test():
    return render_template(
        'test.html',
        title='test',
        year=datetime.now().year,
        message='test page',
        stulist=['a', 'b', 'c', 'd', 'e'],
        amount=list(range(1, 6)),
        stu=db_stu.get_stu_by_id('s001')
    )


# 学生
@app.route('/stu/base_info', methods=['POST'])
def stu_info():
    uname = request.form['uname']
    stu = func.stu_r.stu_info(uname)
    if stu == None:
        return "Log in failed", 403
    else:
        return render_template(
            'student/base_info.html',
            stu=stu,
            stu_id=stu['id'],
            title="学生信息",
            year=datetime.now().year,
        )


@app.route('/stu/course_info', methods=['POST'])
def stu_course_info():
    stu_id = request.form['uname']
    stu_course_list = func.stu_r.stu_course_info(stu_id)
    return render_template(
        'student/course_info.html',
        title='课程成绩',
        stu_course_list=stu_course_list,
        stu_id=stu_id,
        year=datetime.now().year,
    )


# 教师
@app.route('/tea/base_info', methods=['POST'])
def tea_info():
    tea_id = request.form['uname']
    tea = func.tea_r.tea_info(tea_id)
    if tea == None:
        return "Log in failed", 403
    else:
        return render_template(
            'teacher/base_info.html',
            tea=tea,
            tea_id=tea_id,
            title = "教师基本信息",
            year=datetime.now().year,
        )


@app.route('/tea/course_info', methods=['POST'])
def tea_course_info():
    tea_id = request.form.get('uname',None)
    course_id = request.form.get('course_id', None)
    class_id = request.form.get('class_id', None)
    tea = func.tea_r.tea_info(tea_id)
    if not course_id or not class_id:
        return render_template(
            'teacher/course_info.html',
            tea_id=tea_id,
            tea=tea,
            title = "教师课程信息",
            year=datetime.now().year,
        )
    else:
        tcc = func.tea_r.tea_class_course(tea_id, class_id, course_id)
        tcc_json = json.dumps(tcc, ensure_ascii=False)
        return render_template(
            'teacher/course_info.html',
            tea_id=tea_id,
            tea=tea,
            class_id=class_id,
            course_id=course_id,
            class_course=tcc,
            class_course_json=tcc_json,
            title = "教师课程信息",
            year=datetime.now().year,
        )

# 管理员
@app.route('/admin/base_info', methods=['POST'])
def adm_info():
    adm_id = request.form['uname']
    adm = func.adm_r.adm_info(adm_id)
    if adm == None:
        return "Log in failed", 403
    else:
        return render_template(
            'admin/base_info.html',
            adm=adm,
            adm_id=adm_id,
            title = "管理员基本信息",
            year=datetime.now().year,
        ), 200


@app.route('/admin/course_info', methods=['POST'])
def adm_course_info():
    course_id = request.form.get('course_id', None)
    adm_id = request.form.get('uname', None)
    course_list = func.adm_r.course_list()
    if not course_id:
        return render_template(
            '/admin/course_info.html',
            course_list=course_list,
            adm_id=adm_id,
            title = "课程信息",
            year=datetime.now().year,
        ), 200
    else:
        course = func.adm_r.course_info(course_id)
        stu_course_list = func.adm_r.stu_course(course_id)
        tea_course_list = func.adm_r.tea_course(course_id)
        return render_template(
            '/admin/course_info.html',
            course=course,
            course_id=course_id,
            course_list=course_list,
            num_stu_course = len(stu_course_list),
            tea_course_list = tea_course_list,
            adm_id=adm_id,
            title = "课程信息",
            year=datetime.now().year,
        )


@app.route('/admin/stu_info', methods=['POST'])
def adm_stu_info():
    adm_id = request.form.get('uname', None)
    class_id = request.form.get('class_id', None)
    student_id = request.form.get('student_id', None)
    class1_list = func.adm_r.class_list()
    if not class_id:
        return render_template(
            '/admin/stu_info.html',
            adm_id=adm_id,
            class_list=class1_list,
            title = "学生信息",
            year=datetime.now().year,
        ), 200
    elif not student_id:
        stu_list = func.adm_r.class_stu_list(class_id)
        return render_template(
            '/admin/stu_info.html',
            adm_id=adm_id,
            class_list=class1_list,
            class_id=class_id,
            num_stu=len(stu_list),
            stu_list=stu_list,
            title = "学生信息",
            year=datetime.now().year,
        ), 200
    else:
        stu_list = func.adm_r.class_stu_list(class_id)
        student = func.stu_r.stu_info(student_id)
        stu_course_list = func.stu_r.stu_course_info(student_id)
        return render_template(
            '/admin/stu_info.html',
            adm_id=adm_id,
            class_list=class1_list,
            class_id=class_id,
            num_stu=len(stu_list),
            stu_list=stu_list,
            stu_course = stu_course_list,
            student_id=student_id,
            student=student,
            title = "学生信息",
            year=datetime.now().year,
        )


@app.route('/admin/tea_info', methods=['POST'])
def adm_tea_info():
    teacher_id = request.form.get('teacher_id', None)
    adm_id = request.form.get('uname', None)
    teacher_list = func.adm_r.teacher_list()
    if not teacher_id:
        return render_template(
            '/admin/tea_info.html',
            teacher_list=teacher_list,
            adm_id=adm_id,
            title = "教师信息",
            year=datetime.now().year,
        ), 200
    else:
        teacher = func.tea_r.tea_info(teacher_id)
        return render_template(
            '/admin/tea_info.html',
            teacher=teacher,
            teacher_id=teacher_id,
            teacher_list=teacher_list,
            adm_id=adm_id,
            title = "教师信息",
            year=datetime.now().year,
        )


# api
# login
@app.route('/login', methods=['POST'])
def login():
    login_type = request.form['login']
    uname = request.form['uname']
    pw = request.form['pw']
    if login_type == 'stu':
        stu = func.signin.stu_login(uname, pw)
        if stu != None:
            return redirect(url_for('stu_info')), 307
        else:
            return "Log in failed", 403
    elif login_type == 'teacher':
        tea = func.signin.tea_login(uname, pw)
        if tea != None:
            return redirect(url_for('tea_info')), 307
        else:
            return "Log in failed", 403
    elif login_type == 'adm':
        adm = func.signin.adm_login(uname, pw)
        if adm != None:
            return redirect(url_for('adm_info')), 307
        else:
            return "Log in failed", 403
    else:
        return "invalid request type", 403

# 分数录入
@app.route('/score', methods=['POST'])
def up_score():
    stu_id = request.form['student_id']
    course_id = request.form['course_id']
    score_str = request.form.get("score", "-1")
    if not len(score_str):
        return "参数错误", 400
    score = float(score_str)
    if func.tea_w.up_score(stu_id, course_id, score):
        return redirect(url_for('tea_course_info')), 307
    else:
        return "录入失败", 400


@app.route('/admin/add_course', methods=['POST'])
def add_course():
    course_id = request.form.get('course_id', None)
    course_name = request.form.get('course_name', None)
    credit = request.form.get('credit', None)
    if course_id and course_name and credit:
        if func.adm_w.add_course(course_id, course_name, credit):
            return redirect(url_for('adm_course_info')), 307
        else:
            return "添加失败", 400
    else:
        return "参数错误", 400


@app.route('/admin/add_class', methods=['POST'])
def add_class():
    class_id = request.form.get('class_id', None)
    if class_id:
        if func.adm_w.add_class(class_id):
            return redirect(url_for('adm_stu_info')), 307
        else:
            return "添加失败", 400
    else:
        return "参数错误", 400


@app.route('/admin/add_student', methods=['POST'])
def add_student():
    student_id = request.form.get('student_id', None)
    studetn_name = request.form.get('name', None)
    sex = request.form.get('sex', None)
    birthdate = request.form.get('birth_date', None)
    entrance_date = request.form.get('entrance_date', None)
    class_id = request.form.get('class_id')
    if student_id and class_id:
        if func.adm_w.add_stu(student_id, studetn_name, sex, birthdate, entrance_date, class_id):
            return redirect(url_for('adm_stu_info')), 307
        else:
            return "添加失败", 400
    else:
        return "参数错误", 400

@app.route('/admin/mod_course', methods=['POST'])
def mod_course():
    course_id = request.form.get('course_id', None)
    course_name = request.form.get('course_name', None)
    credit = request.form.get('credit', None)
    if course_id and course_name and credit:
        if func.adm_w.mod_course(course_id, course_name, credit):
            return redirect(url_for('adm_course_info')), 307
        else:
            return "修改失败", 400
    else:
        return "参数错误", 400

@app.route('/admin/del_course', methods=['POST'])
def del_course():
    course_id = request.form.get('course_id_to_del')
    if course_id:
        if func.adm_w.del_course(course_id):
            return redirect(url_for('adm_course_info')), 307
        else:
            return "删除失败", 400
    else:
        return "参数错误", 400

@app.route('/admin/del_stu', methods=['POST'])
def del_stu():
    stu_id = request.form.get('stu_id_to_del')
    if stu_id:
        if func.adm_w.del_stu(stu_id):
            return redirect(url_for('adm_stu_info')), 307
        else:
            return "删除失败", 400
    else:
        return "参数错误", 400

@app.route('/admin/del_class', methods=['POST'])
def del_class():
    class_id = request.form.get('class_id_to_del')
    if class_id:
        if func.adm_w.del_class(class_id):
            return redirect(url_for('adm_stu_info')), 307
        else:
            return "删除失败", 400
    else:
        return "参数错误", 400

@app.route('/admin/mod_stu',methods=['POST'])
def mod_stu():
    student_id = request.form.get('student_id', None)
    studetn_name = request.form.get('name', None)
    sex = request.form.get('sex', None)
    birthdate = request.form.get('birth_date', None)
    entrance_date = request.form.get('entrance_date', None)
    class_id = request.form.get('class_id',None)
    if student_id:
        if func.adm_w.mod_stu(student_id, studetn_name, sex, birthdate, entrance_date,class_id):
            return redirect(url_for('adm_stu_info')), 307
        else:
            return "修改失败", 400
    else:
        return "参数错误", 400


@app.route('/admin/add_teacher', methods=['POST'])
def add_teacher():
    teacher_id = request.form.get("teacher_id",None)
    teacher_name = request.form.get("name",None)
    if teacher_id:
        if func.adm_w.add_tea(teacher_id,teacher_name):
            return redirect(url_for('adm_tea_info')), 307
        else:
            return "添加失败", 400
    else:
        return "参数错误", 400

@app.route('/admin/mod_teacher', methods=['POST'])
def mod_teacher():
    teacher_id = request.form.get("teacher_id",None)
    teacher_name = request.form.get("name",None)
    if teacher_id:
        if func.adm_w.mod_tea(teacher_id,teacher_name):
            return redirect(url_for('adm_tea_info')), 307
        else:
            return "修改失败", 400
    else:
        return "参数错误", 400

@app.route('/admin/del_teacher', methods=['POST'])
def del_teacher():
    teacher_id = request.form.get('tea_id_to_del',None)
    if teacher_id:
        if func.adm_w.del_teacher(teacher_id):
            return redirect(url_for('adm_tea_info')), 307
        else:
            return "删除失败", 400
    else:
        return "参数错误", 400