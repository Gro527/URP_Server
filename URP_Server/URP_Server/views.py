"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request,redirect,url_for
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
        stulist = ['a','b','c','d','e'],
        amount = list(range(1,6)),
        stu = db_stu.get_stu_by_id('s001')
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
            stu = stu,
            stu_id = stu['id'],
            title = "学生信息"
        )

@app.route('/stu/course_info', methods=['POST'])
def stu_course_info():
    stu_id = request.form['uname']
    stu_course_list = func.stu_r.stu_course_info(stu_id)
    return render_template(
        'student/course_info.html',
        title = '课程成绩',
        stu_course_list = stu_course_list,
        stu_id = stu_id
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
            tea = tea,
            tea_id = tea_id
        )

@app.route('/tea/course_info', methods=['POST'])
def tea_course_info():
    tea_id = request.form['uname']
    course_id = request.form.get('course_id',None)
    class_id = request.form.get('class_id',None)
    tea = func.tea_r.tea_info(tea_id)
    print(request.form)
    if not course_id or not class_id:
        return render_template(
            'teacher/course_info.html',
            tea_id = tea_id,
            tea = tea
        )
    else:
        tcc = func.tea_r.tea_class_course(tea_id,class_id,course_id)
        tcc_json = json.dumps(tcc, ensure_ascii=False)
        print(tcc ,tcc_json)
        return render_template(
            'teacher/course_info.html',
            tea_id = tea_id,
            tea = tea,
            class_id = class_id,
            course_id = course_id,
            class_course = tcc,
            class_course_json = tcc_json
        )



















# api
# login
@app.route('/login', methods=['POST'])
def login():
    login_type = request.form['login']
    uname = request.form['uname']
    pw = request.form['pw']
    if login_type == 'stu':
        stu = func.signin.stu_login(uname,pw)
        if stu != None:
            return redirect(url_for('stu_info')),307
    elif login_type == 'teacher':
        tea = func.signin.tea_login(uname,pw)
        if tea != None:
            return redirect(url_for('tea_info')), 307
    elif login_type == 'adm':
        return redirect(url_for('adm_page')),307
    else:
        return "invalid request type", 403

# 分数录入
@app.route('/score', methods=['POST'])
def up_score():
    print(request.form)
    stu_id = request.form['student_id']
    course_id = request.form['course_id']
    score = request.form['score']
    if func.tea_w.up_score(stu_id,course_id,score):
        return "录入成功"
    else:
        return "录入失败",500