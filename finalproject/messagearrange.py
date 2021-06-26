from flask import Flask, render_template, url_for, request, json,jsonify
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_sqlalchemy import SQLAlchemy
# import configs01
import os
UPLOAD_FOLDER = 'uploads'
bp = Blueprint('messagearrange', __name__,url_prefix='/messagearrange')
from database import get_db
from models import User, Course
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
# app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
# app.config.from_object(configs01)
# db = SQLAlchemy(app)

# from models import User, Course
'''
class User:
    def __init__(self, uid, sex, age, name, status):
        self.uid = uid
        self.sex = sex
        self.age = age
        self.name = name
        self.status = status

class Course:
    def __init__(self, name, description, credit, capacity, cid, instructor, type, time, classroom):
        self.name = name
        self.description = description
        self.credit = credit
        self.capacity = capacity
        self.cid = cid
        self.instructor = instructor
        self.type = type
        self.time = time
        self.classroom = classroom
'''
#
# class User(db.Model):
#     __bind_key__ = 'course_arrangement_system'
#     __tablename__ = 'user'
#     uid = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(45))
#     sex = db.Column(db.String(25))
#     age = db.Column(db.Integer)
#     status = db.Column(db.String(45))
#     def __repr__(self):
#         return '<user>{}:{}:{}:{}:{}'.format(self.uid,self.name,self.sex,self.age,self.status)
#
# class Course(db.Model):
#     __bind_key__ = 'course_arrangement_system'
#     __tablename__ = 'course'
#     cid = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(45))
#     credit = db.Column(db.Integer)
#     capacity = db.Column(db.Integer)
#     instructor = db.Column(db.String(45))
#     type = db.Column(db.String(20))
#     time = db.Column(db.String(45))
#     classroom = db.Column(db.String(45))
#     description = db.Column(db.String(255))
#     def __repr__(self):
#         return '<course>{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.cid, self.name, self.credit, self.capacity, self.instructor,self.type, self.time, self.classroom, self.description)

@bp.route('/')
def hello_world():
    return render_template('sidebar.html')

@bp.route('/personal-center.html', methods=['GET', 'POST'])
def personal_center():
    u = User.query.filter((User.uid) == (current_user.uid)).first()
    return render_template("MessageArrange/personal-center.html", user = u)

@bp.route('/EditInfo', methods=['GET', 'POST'])
def EditInfo():
    name = request.form.get('name')
    age = request.form.get('age')
    sex = request.form.get('sex')
    uid = current_user.uid
    error = None
    if name == '':
        error = "未输入姓名"
    elif age == '':
        error = "未输入年龄"
    elif sex == '':
        error = "未输入性别"
    elif age <= '0' :
        error = "年龄不能小于0"
    else:
        u = User.query.filter(User.uid == uid).first()
        u.name = name
        u.age = age
        u.sex = sex
        db = get_db()
        db.session.commit()

    if(error):
        flash(error)
    else:
        flash('修改成功')
    return redirect(url_for('messagearrange.course_search'))


@bp.route('/course-information.html/<cid>', methods=['GET', 'POST'])
def course_information(cid):
    print(str(cid))
    c = Course.query.filter(Course.cid==cid).first()
    return render_template("MessageArrange/course-information.html", course = c)

@bp.route('/course-search.html', methods=['GET', 'POST'])
def course_search():
    c = Course.query.all()
    return render_template("MessageArrange/course-search.html", courses=c)

@bp.route('EditCourse', methods=['GET', 'POST'])
def EditCourse():
    cid = request.form.get('cid')
    name = request.form.get('name')
    time = request.form.get('time')
    classroom = request.form.get('classroom')
    instructor = request.form.get('instructor')
    credit = request.form.get('credit')
    type = request.form.get('type')
    description = request.form.get('description')
    capacity = request.form.get('capacity')
    error = None

    if name == '' :
        error = '未输入课程名'
    elif time == '':
        error = '未输入上课时间'
    elif classroom == '':
        error = '未输入上课教室'
    elif instructor == '':
        error = '未输入教师'
    elif credit == '':
        error = '未输入学分'
    elif type == '':
        error = '未输入课程类型'
    elif description == '':
        error = '未输入课程描述'
    elif capacity == '':
        error = '未输入课程容量'
    else:
        db = get_db()
        c = Course.query.filter(Course.cid == cid).first()
        c.name = name
        c.time = time
        c.classroom = classroom
        c.instructor = instructor
        c.credit = credit
        c.type = type
        c.description = description
        c.capacity = capacity
        db.session.commit()
    if error:
        flash(error)
    else:
        flash('修改成功')

    c = Course.query.all()
    return render_template("MessageArrange/course-search.html", courses=c)

@bp.route('EditUser', methods=['GET', 'POST'])
def EditUser():
    uid = request.form.get('uid')
    name = request.form.get('name')
    sex = request.form.get('sex')
    age = request.form.get('age')
    status = request.form.get('status')
    error = None

    if uid == '' :
        error = '未输入学工号'
    elif name == '':
        error = '未输入姓名'
    elif sex == '':
        error = '未输入性别'
    elif age == '':
        error = '未输入年龄'
    elif status == '':
        error = '未输入身份'
    else:
        db = get_db()
        u = User.query.filter(User.uid == uid).first()
        print((name))
        u.name = name
        u.age = age
        u.sex = sex
        u.status = status
        db.session.commit()
    if error:
        flash(error)
    else:
        flash('修改成功')

    u = User.query.all()
    return render_template("MessageArrange/user-search.html", users=u)

@bp.route('/course-delete/<cid>', methods=['GET', 'POST'])
def DeleteCourse(cid):
    delete_course = Course.query.filter(Course.cid == cid).first()
    db = get_db()
    db.session.delete(delete_course)
    db.session.commit()

    c = Course.query.all()
    flash('成功删除')
    return redirect(url_for("messagearrange.course_search"))
    # return render_template("course-search.html", courses=c)

@bp.route('/user-delete/<uid>', methods=['GET', 'POST'])
def DeleteUser(uid):
    delete_user = User.query.filter(User.uid == uid).first()
    db = get_db()
    db.session.delete(delete_user)
    db.session.commit()
    flash('成功删除')
    return redirect(url_for("messagearrange.user_search"))
    # return render_template("course-search.html", courses=c)

@bp.route('/AddCourse', methods=['GET', 'POST'])
def AddCourse():
    name = request.form.get('name')
    cid = request.form.get('cid')
    time = request.form.get('time')
    classroom = request.form.get('classroom')
    instructor = request.form.get('instructor')
    credit = request.form.get('credit')
    type = request.form.get('type')
    description = request.form.get('description')
    capacity = request.form.get('capacity')
    error = None

    if name == '':
        error = '未输入课程名'
    elif cid == '':
        error = '未输入课程编号'
    elif time == '':
        error = '未输入上课时间'
    elif classroom == '':
        error = '未输入上课教室'
    elif instructor == '':
        error = '未输入教师'
    elif credit == '':
        error = '未输入学分'
    elif type == '':
        error = '未输入课程类型'
    elif description == '':
        error = '未输入课程描述'
    elif capacity == '':
        error = '未输入课程容量'
    else:
        NewCourse = Course(name=name, description=description, credit=credit, capacity=capacity, cid=cid,
                           instructor=instructor, type=type, time=time, classroom=classroom)
        db = get_db()
        db.session.add(NewCourse)
        db.session.commit()
    if error:
        flash(error)
    else:
        flash('成功添加')
    c = Course.query.all()
    return render_template("MessageArrange/course-search.html", courses=c)


@bp.route('/user-search.html', methods=['GET', 'POST'])
def user_search():
    #u = [User('1','2','3','4','5'), User('5','4','3','2','1')]
    u = User.query.all()
    return render_template("MessageArrange/user-search.html", users=u)

@bp.route('/AddUser', methods=['GET', 'POST'])
def AddUser():
    uid = request.form.get('uid')
    name = request.form.get('name')
    age = request.form.get('age')
    sex = request.form.get('sex')
    status = request.form.get('status')
    error = None
    if name == '':
        error = "未输入姓名"
    elif uid == '':
        error = '未输入学工号'
    elif age == '':
        error = "未输入年龄"
    elif sex == '':
        error = "未输入性别"
    elif status == '':
        error = '未输入身份'
    elif age <= '0':
        error = "年龄不能小于0"
    else:
        db = get_db()
        NewUser = User(uid=uid, name=name, age=age, sex=sex,status=status, password='123456')
        db.session.add(NewUser)
        db.session.commit()
    u = User.query.all()
    if (error):
        flash(error)
    else:
        flash('添加成功')
    return render_template("MessageArrange/user-search.html", users=u)


@bp.route('/SubmitPhoto', methods=['GET', 'POST'])
def SubmitPhoto():
    photo = request.files['photo']
    u = User.query.filter(User.uid == current_user.uid).first()
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = basedir + "\\static\\assets\\images\\lg\\" + str(u.uid) + '.jpg'
    photo.save(file_path)
    return render_template("MessageArrange/personal-center.html", user=u)

'''
@app.route('/')
def hello_world():
    user1 = User(uid=100,sex='nan',age=10,status="sss",name='lou')
    db.session.add(user1)
    db.session.commit()
    return 'Hello World!'
'''
# if __name__ == '__main__':
#
#     app.run()