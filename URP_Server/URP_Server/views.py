"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request,redirect,url_for
from URP_Server import app
from URP_Server.db import db_stu
from URP_Server import func


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


@app.route('/stu/base_info', methods=['POST'])
def stu_info():
    uname = request.form['uname']
    stu = func.stu_r.stu_info(uname)
    if stu == None:
        return "Log in failed", 403
    else:
        return render_template(
            'student/info.html',
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
    
@app.route('/teacher', methods=['POST'])
def tea_page():
    uname = request.form['uname']
    pw = request.form['pw']
    tea = func.signin.tea_login(uname,pw)
    if tea == None:
        return "Log in failed", 403
    else:
        return render_template(
            'teacher.html',
            tea = tea
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
    elif login_type == 'tea':
        return redirect(url_for('tea_page')), 307
    elif login_type == 'adm':
        return redirect(url_for('adm_page')),307