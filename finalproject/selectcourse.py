from flask import Flask, render_template, flash, request, redirect, url_for, session, send_from_directory, Blueprint,current_app
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from operator import attrgetter
import pymysql
from sqlalchemy.orm import relationship
from datetime import datetime
import os
#from flask_login import LoginManager, current_user, login_user, login_required
# app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://用户名:密码@127.0.0.1:3306/数据库名'
#host:rm-2zeb626gl3ajx1372ho.mysql.rds.aliyuncs.com
#username: fse_g7
#password:FSE_group7
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://fse_g7:FSE_group7@rm-2zeb626gl3ajx1372ho.mysql.rds.aliyuncs.com:3306/select_course'
# #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'hahhahahhah'
# app.config['UPLOAD_FOLDER'] = "培养方案"

# db = SQLAlchemy(app)
from models import Student, StudentToCourse, Course_3, BEApplication, Teacher_3, Major
from database import get_db
SelCourseStart = datetime (2020, 1, 1)       # Normal Course Selection 初选
SelCourseEnd = datetime (2021, 10, 10)

BESelCourseStart = datetime (2020, 1, 1)     # By Election Course Selection 补课
BESelCourseEnd = datetime (2021, 10, 10)
UPLOAD_FOLDER = '培养方案'
bp = Blueprint('selectcourse', __name__, url_prefix='/selectcourse')


#############
#   数据库
############
#
# class Student(db.Model):
#     __tablename__ = 'student'
#     id = db.Column(db.Integer, primary_key=True)    #主键
#     name = db.Column(db.String(16), unique=True)
#     gender = db.Column(db.Enum("男", "女"), nullable=False)
#     major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
#     courses = db.relationship("Course", secondary="student_to_course", backref="students")
#     applications = db.relationship("Course", secondary="application", backref="astudents")
#
# class StudentToCourse(db.Model):
#     __tablename__ = 'student_to_course'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
#     course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
#
# class Course_3(db.Model):
#     __tablename__ = 'course'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(16), unique=True)
#     time = db.Column(db.String(10), nullable=False)
#     curr_capacity = db.Column(db.Integer, default=0)
#     max_capacity = db.Column(db.Integer, default=60)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
#
# class BEApplication(db.Model):      #student's application for by-election
#     __tablename__ = 'application'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
#     course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
#
# class Teacher_3(db.Model):
#     __tablename__ = 'teacher'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(16), unique=True)
#     courses = relationship('Course', backref='teacher')
#
# class Major(db.Model):
#     __tablename__ = 'major'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), unique=True)
#     students = db.relationship("Student", backref="major")
#
# class Administrator(db.Model):
#     __tablename__ = 'administrator'
#     id= db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(16), unique=True)
#db.drop_all()
#db.create_all()
#############
#    教师
############

@bp.route('/studentlist/<course_id>', methods=['GET', 'POST'])
def studentlist(course_id):
    try:
        course = Course_3.query.filter(Course_3.id == course_id).first()
    except BaseException as e:
        print(e)
        flash('数据库操作失败')
        return render_template('SelectCourse/studentlist.html', students=None, astudents=None, course_id=course_id)

    return render_template('SelectCourse/studentlist.html', students=course.students, astudents=course.astudents, course_id=course_id)

@bp.route('/myclass', methods=['GET'])
def myclass():
    print(current_user.id)
    try:
        courses = Course_3.query.filter(Course_3.teacher_id == current_user.id).all()
        for i in courses:
            print(i.name)
    except BaseException as e:
        flash("数据库查询失败")
        return redirect(url_for('myclass'))

    return render_template('SelectCourse/tcourses.html', courses=courses,
                days={"1": "星期一", "2": "星期二", "3": "星期三", "4": "星期四", "5": "星期五", "6": "星期六", "7": "星期日"},
                time={"A": "10", "B": "11", "C": "12", "D": "13"})
    # else:
    #     flash('不存在这个session')
    #     return render_template('tcourses.html',
    #         days={"1": "星期一", "2": "星期二", "3": "星期三", "4": "星期四", "5": "星期五", "6": "星期六", "7": "星期日"},
    #         time={"A": "10", "B": "11", "C": "12", "D": "13"})

@bp.route('/acceptapp/<course_id>/<student_id>', methods=['GET', 'POST'])
def acceptapp(student_id, course_id):
    # 更新课程容量
    tempCourse = Course_3.query.get(course_id)
    tempCourse.curr_capacity = tempCourse.curr_capacity + 1

    BEApplication.query.filter_by(course_id=course_id, student_id=student_id).delete()
    s = StudentToCourse(student_id=student_id, course_id=course_id)
    db = get_db()
    try:
        db.session.add(s)
        db.session.commit()
    except:
        flash('fuck')
    return redirect(url_for('studentlist', course_id=course_id))

@bp.route('/rejectapp/<course_id>/<student_id>', methods=['GET', 'POST'])
def rejectapp(student_id, course_id):
    BEApplication.query.filter_by(course_id=course_id, student_id=student_id).delete()
    db.session.commit()
    return redirect(url_for('studentlist', course_id=course_id))
############
#  学生
############

@bp.route('/download/<path:filename>')
def download(filename):
    '''downloads 培养方案
    -(filename needs the filetype ex.Example.pdf)
'''
    fullpath = os.path.join (current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    return send_from_directory(fullpath, filename)

@bp.route('/inquiry_courses', methods = ["GET", "POST"])
def inquiry_courses():
    '''课程查询
        -user can select a search method (ALL COURSES, class ID, name, teacherID, time)
        -user then inputs data regarding that search method
        -the function will output the related courses if found
         '''
    if session['student_id'] == 0:
        flash("不存在这个Session")
        return render_template("inquiry_courses.html", courses=[], user=session['user'],
               days={"1": "星期一", "2": "星期二", "3": "星期三", "4": "星期四", "5": "星期五", "6": "星期六", "7": "星期日"},
               time={"A": "10", "B": "11", "C": "12", "D": "13"})

    courses = Course_3.query.all()

    isValid = True
    if request.method == "POST":
        Option = request.form["Option"]
        inquiry = request.form["inquiry"]
        if Option == "All":
            courses = Course_3.query.all()

        elif Option == "ID":
            try:
                inquiry = int(inquiry)
            except ValueError :
                isValid = False        #输入不合法
            if isValid:
                courses = Course_3.query.filter(Course_3.id == inquiry).all()
            else:
                flash ("课程ID不符合格式")
                courses = []

        elif Option == "Name":
            courses = Course_3.query.filter(Course_3.name == inquiry).all()

        elif Option == "Teacher_Id":
            try:
                inquiry = int(inquiry)
            except ValueError :
                isValid = False        #输入不合法
            if isValid:
                courses = Course_3.query.filter(Course_3.teacher_id == inquiry).all()
            else:
                flash("老师ID不符合格式")

        elif Option == "Teacher_Name":
            courses = []
            for tempc in Course_3.query.all():
                if inquiry == Teacher_3.query.get(tempc.teacher_id).name:
                    courses.append(tempc)

        elif Option == "Time":
            courses = []
            days = {"星期一": "1", "星期二": "2", "星期三": "3", "星期四": "4", "星期五": "5", "星期六": "6", "星期日": "7"}
            if inquiry in days:
                for tempc in Course_3.query.all():
                    if tempc.time[4] == days[inquiry] or tempc.time[7] == days[inquiry]:
                        courses.append(tempc)
            else:
                flash ("输入格式为：星期一  ~  日")

        if (isValid and courses):
            return render_template("SelectCourse/inquiry_courses.html", courses=courses, user=session['user'],
                    days={"1": "星期一", "2": "星期二", "3": "星期三", "4": "星期四", "5": "星期五", "6": "星期六", "7": "星期日"},
                    time={"A": "10", "B": "11", "C": "12", "D": "13"})

    return render_template("SelectCourse/inquiry_courses.html", courses=courses, user=session['user'],
                    days={"1": "星期一", "2": "星期二", "3": "星期三", "4": "星期四", "5": "星期五", "6": "星期六", "7": "星期日"},
                    time={"A": "10", "B": "11", "C": "12", "D": "13"})

@bp.route('/inquiry_major', methods = ["GET", "POST"])
def inquiry_major():
    '''课程查询
        -user can select a search method (ALL COURSES, major name)
        -user then inputs data regarding that search method
        -the function will output the related major if found
         '''

    Majors = None

    if request.method == "POST":
        Option = request.form["Option"]
        inquiry = request.form["inquiry"]
        if Option == "All":
            Majors = Major.query.all()
        elif Option == "mine":
            student_id = session['student_id']
            tempStu = Student.query.get(student_id)
            major_id = tempStu.major_id
            Majors = Major.query.filter(Major.id == major_id).all()
        elif Option == "Name":
            Majors = Major.query.filter(Major.name == inquiry).all()

        if Majors:
            return render_template("SelectCourse/inquiry_major.html", Majors=Majors, user=session['user'])

    return render_template("SelectCourse/inquiry_major.html", Majors=Majors, user=session['user'])

@bp.route('/selcourse/<course_id>', methods=["GET", "POST"])
def sel_course(course_id):
    '''adds a course into a student's timetable
    -used by Student
    -function can only run during initial course selection period
    '''

    student_id = session['student_id']
    currDatetime = datetime.now()

    if currDatetime < SelCourseStart or currDatetime > SelCourseEnd:  # 不是选课时间
        flash ("现在不是选课时间")
        return render_template("SelectCourse/inquiry_courses.html")

    tempStu = Student.query.get(student_id)
    tempCourse = Course_3.query.get(course_id)

    # next three if statements are for edge cases
    if tempStu is None:  # 学生不存在
        flash ("学生不存在")
        return redirect(url_for('inquiry_courses'))

    if tempCourse is None:  # 课程不存在
        flash ("课程不存在")
        return redirect(url_for('inquiry_courses'))
    if tempCourse in tempStu.courses:   # 学生已选上这门课
        flash ("学生已经选这门课")
        return redirect(url_for('inquiry_courses'))
    if tempCourse.curr_capacity >= tempCourse.max_capacity:   # 课程没有余量
        flash ("课程学生容量过多")
        return redirect(url_for('inquiry_courses'))
    for course in tempStu.courses:  # 找时间冲突
        if course.time[0:1] == tempCourse.time[0:1]:  # 两门课的学年相同
            if course.time[2] in tempCourse.time[2:4] or course.time[3] in tempCourse.time[2:4]:  # 两门课有共同学期
                if course.time[4:7] == tempCourse.time[4:7] or \
                        course.time[4:7] == tempCourse.time[7:10] or \
                        course.time[7:10] == tempCourse.time[4:7] or \
                        course.time[7:10] == tempCourse.time[7:10] \
                        :  # 两门课有时间冲突
                    flash ("有时间冲突")
                    return redirect(url_for('inquiry_courses'))
    # 进行选课
    tempCourse.curr_capacity = tempCourse.curr_capacity + 1
    tempCourse.students.append(tempStu)
    db = get_db()
    db.session.commit()
    flash("选课成功！")
    return redirect(url_for('inquiry_courses'))

@bp.route('/BEselcourse/<course_id>', methods=["GET", "POST"])
def BEsel_course(course_id):
    '''allows student user to create a by-election application
    -can only be used during by-selection period
    -student must be able to fit the course into their timetable
    for this function to run
    '''
    student_id = session['student_id']
    currDatetime = datetime.now()

    if currDatetime < BESelCourseStart or currDatetime > BESelCourseEnd:  # 不是选课时间
        flash ("现在不是补选时间")
        return redirect(url_for('inquiry_courses'))
        
    tempStu = Student.query.get(student_id)
    tempCourse = Course_3.query.get(course_id)

    # next three if statements are for edge cases
    if tempStu is None:  # 学生不存在
        flash ("学生不存在")
        return redirect(url_for('inquiry_courses'))

    if tempCourse is None:  # 课程不存在
        flash ("课程不存在")
        return redirect(url_for('inquiry_courses'))

    if tempCourse in tempStu.courses:  # 学生已选上这门课
        flash ("学生已经选这门课")
        return redirect(url_for('inquiry_courses'))

    # 学生已补选上这门课
    if BEApplication.query.filter(BEApplication.student_id == student_id, BEApplication.course_id == course_id).first():
        #print("Course is already BEselected")
        flash ("学生已经补选这门课")
        return redirect(url_for('inquiry_courses'))

    for course in tempStu.courses:  # 找时间冲突
        if course.time[0:1] == tempCourse.time[0:1]:  # 两门课的学年相同
            #print("SAME YEAR")
            if course.time[2] in tempCourse.time[2:4] or course.time[3] in tempCourse.time[2:4]:  # 两门课有共同学期
                #print("SAME SEMESTER")
                if course.time[4:7] == tempCourse.time[4:7] or \
                        course.time[4:7] == tempCourse.time[7:10] or \
                        course.time[7:10] == tempCourse.time[4:7] or \
                        course.time[7:10] == tempCourse.time[7:10] \
                        :  # 两门课有时间冲突
                    flash ("有时间冲突")
                    return redirect(url_for('inquiry_courses'))

    # Creating new relation
    tempApplication = BEApplication (student_id=student_id, course_id=course_id)
    db = get_db()
    db.session.add (tempApplication)
    db.session.commit ()

    flash ("补选成功！")
    return redirect(url_for('inquiry_courses'))

@bp.route('/BEappManage', methods=["GET"])
def BEappManage():
    '''shows student all of their by-election applications
    -used by students
    '''
    student_id = session['student_id']
    applications = BEApplication.query.filter(BEApplication.student_id == student_id).all()
    return render_template("SelectCourse/myBEAppl.html", applications=applications, user=session['user'])

@bp.route('/deleteBEApplication/<course_id>', methods=["GET", "POST"])
def deleteBEappl(course_id):
    '''deletes a student's by-election application for a course
    -used by Student'''
    student_id = session['student_id']
    BEApplication.query.filter(BEApplication.student_id == student_id, BEApplication.course_id == course_id).delete()
    db = get_db()
    db.session.commit()

    flash("补选申请删除成功！")
    return redirect(url_for('BEappManage'))

@bp.route('/delcourse/<course_id>', methods=["GET", "POST"])
def del_course(course_id):
    '''deletes a course from a student's time table
    -used by Student
    '''
    student_id = session['student_id']
    currDatetime = datetime.now()

    if currDatetime < SelCourseStart or currDatetime > SelCourseEnd:  # 不是选课时间
        flash("现在不是选课时间")
        return redirect(url_for('inquiry_courses'))
    tempStu = Student.query.get(student_id)
    tempCourse = Course_3.query.get(course_id)

    # Below two checks may be optional? depends if there is a case where the ids don't exist
    if tempStu == None:  # 学生不存在
        flash ("学生不存在")
        return redirect(url_for('inquiry_courses'))

    if tempCourse == None:  # 课程不存在
        flash ("课程不存在")
        return redirect(url_for('inquiry_courses'))

    if tempCourse not in tempStu.courses:   # 课未选上
        flash ("学生没选上本课程")
        return redirect(url_for('inquiry_courses'))

    # 进行退课
    tempCourse.students.remove(tempStu)
    tempCourse.curr_capacity = tempCourse.curr_capacity - 1
    db = get_db()
    db.session.commit()
    flash ("退课成功！")
    return redirect(url_for('inquiry_courses'))

# 从mycurriculum网页进行退课功能
@bp.route('/delcourse2/<course_id>', methods=["GET", "POST"])
def del_course2(course_id):
    '''deletes a course from a student's time table
    -used by Student
    '''
    student_id = session['student_id']
    currDatetime = datetime.now()

    if currDatetime < SelCourseStart or currDatetime > SelCourseEnd:  # 不是选课时间
        flash("现在不是选课时间")
        return redirect(url_for('inquiry_courses'))
    tempStu = Student.query.get(student_id)
    tempCourse = Course_3.query.get(course_id)

    if tempStu == None:  # 学生不存在
        flash ("学生不存在")
        return redirect(url_for('inquiry_courses'))

    # 进行退课
    tempCourse.students.remove(tempStu)
    tempCourse.curr_capacity = tempCourse.curr_capacity - 1
    db = get_db()
    db.session.commit()
    flash ("退课成功！")
    return redirect(url_for('mycurriculum'))

@bp.route('/mycurriculum', methods = ['GET'])
def mycurriculum():
    '''shows student's list of selected courses
    and a timetable for each season with their selected courses
    '''
    student_id = session['student_id']
    tempStu = Student.query.get(student_id)
    Courses = sorted(tempStu.courses, key=attrgetter("id"))

    timetable = \
        [
            [
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', '']
            ],
            [
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', '']
            ],
            [
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', '']
            ],
            [
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', '']
            ]
        ]

    for tempCourse in Courses:
        for i in range(int(tempCourse.time[2], 10), int(tempCourse.time[3], 10) + 1):
            for j in range(int(tempCourse.time[5], 16), int(tempCourse.time[6], 16) + 1):
                timetable[i - 1][int(tempCourse.time[4], 10) - 1][j - 1] = tempCourse.name
            for j in range(int(tempCourse.time[8], 16), int(tempCourse.time[9], 16) + 1):
                timetable[i - 1][int(tempCourse.time[7], 10) - 1][j - 1] = tempCourse.name

    return render_template('SelectCourse/student_courses.html', courses=Courses, tStudent=tempStu, user=session['user'],
        timetable=timetable,
        days={"1": "星期一", "2": "星期二", "3": "星期三", "4": "星期四", "5": "星期五", "6": "星期六", "7": "星期日"},
        time={"A": "10", "B": "11", "C": "12", "D": "13"})

############
#   管理员
############
@bp.route('/admin_selcourse', methods=["GET", "POST"])
def admin_sel_course():
    '''adds a course into a student's timetable
    -used by admins
    -used anytime
    '''

    student_id = None
    course_id = None
    isFresh = True

    if request.method == "POST":
        student_id = request.form["Student_ID"]
        course_id = request.form["Course_ID"]

        if (student_id == '' and course_id == ''):
            flash("失败！没有输入")
            return render_template("SelectCourse/admin_sel_course.html", student_id=student_id, course_id=course_id, user=session['user'])
        try:
            student_id = int(student_id)
            course_id = int(course_id)
            isFresh = False
        except ValueError:
            flash("失败！输入ID不符合格式")
            return render_template("SelectCourse/admin_sel_course.html", student_id=student_id, course_id=course_id,user=session['user'])
    tempStu = Student.query.get(student_id)
    tempCourse = Course_3.query.get(course_id)

    if tempStu is None:  # 学生不存在
        if isFresh == False:
            flash("失败！学生不存在")
        return render_template("SelectCourse/admin_sel_course.html", student_id=student_id, course_id=course_id, user=session['user'])

    if tempCourse is None:  # 课程不存在
        flash("失败！课程不存在")
        return render_template("SelectCourse/admin_sel_course.html", student_id=student_id, course_id=course_id, user=session['user'])

    if tempCourse in tempStu.courses:  # 学生已选上这门课
        flash("失败！学生已经在课程")
        return render_template("SelectCourse/admin_sel_course.html", student_id=student_id, course_id=course_id, user=session['user'])

    if tempCourse.curr_capacity >= tempCourse.max_capacity:  # 课程没有余量
        # Maybe we should still allow admins to put students in courses that are full
        flash("失败！课程学生容量过多")
        return render_template("SelectCourse/admin_sel_course.html", student_id=student_id, course_id=course_id, user=session['user'])

    for course in tempStu.courses:  # 找时间冲突
        if course.time[0:1] == tempCourse.time[0:1]:  # 两门课的学年相同
            if course.time[2] in tempCourse.time[2:4] or course.time[3] in tempCourse.time[2:4]:  # 两门课有共同学期
                if course.time[4:7] == tempCourse.time[4:7] or \
                        course.time[4:7] == tempCourse.time[7:10] or \
                        course.time[7:10] == tempCourse.time[4:7] or \
                        course.time[7:10] == tempCourse.time[7:10] \
                        :  # 两门课有时间冲突
                    flash("Failed. There are time conflicts")
                    return render_template("SelectCourse/admin_sel_course.html", student_id=student_id, course_id=course_id, user=session['user'])

    # 进行选课

    # 通过补选接受补选，需要删除学生补选申请
    BEApplication.query.filter(BEApplication.student_id == student_id, BEApplication.course_id == course_id).delete()

    tempCourse.curr_capacity = tempCourse.curr_capacity + 1
    tempCourse.students.append(tempStu)
    db = get_db()
    db.session.commit()

    flash("手动选课成功！" + tempCourse.name + "加入了" + tempStu.name + "的课表")
    return render_template("SelectCourse/admin_sel_course.html", student_id=student_id, course_id=course_id, user=session['user'])

@bp.route('/admin_delcourse', methods = ["GET", "POST"])
def admin_del_course():
    '''deletes a course from a student's timetable
    -used by admins
    -used anytime
    '''

    student_id = None
    course_id = None
    isFresh = True
    if request.method == "GET":
        return render_template("SelectCourse/admin_del_course.html", user=session['user'])

    if request.method == "POST":
        student_id = request.form["Student_ID"]
        course_id = request.form["Course_ID"]
        isFresh=False

        if (student_id == '' and course_id == ''):
            flash("失败！没有输入")
            return render_template("SelectCourse/admin_del_course.html", student_id=student_id, course_id=course_id, user=session['user'])
        try:
            student_id = int(student_id)
            course_id = int(course_id)
        except ValueError:
            flash("失败！输入ID不符合格式")

    tempStu = Student.query.get(student_id)
    tempCourse = Course_3.query.get(course_id)

    if tempStu is None:  # 学生不存在
        if isFresh == False:
            flash("失败！学生不存在")
            return render_template("SelectCourse/admin_del_course.html", student_id=student_id, course_id=course_id, user=session['user'])

    if tempCourse is None:  # 课程不存在
        flash("失败！课程不存在")
        return render_template("SelectCourse/admin_del_course.html", student_id=student_id, course_id=course_id, user=session['user'])

    if tempCourse not in tempStu.courses:  # 课未选上
        flash("失败！学生不在课程")
        return render_template("SelectCourse/admin_del_course.html", student_id=student_id, course_id=course_id, user=session['user'])

    tempCourse.students.remove(tempStu)
    tempCourse.curr_capacity = tempCourse.curr_capacity - 1
    db = get_db()
    db.session.commit()

    flash("手动退课成功！")
    return render_template("SelectCourse/admin_del_course.html", student_id=student_id, course_id=course_id, user=session['user'])

@bp.route('/changeSelCoursePeriod', methods = ["GET", "POST"])
def changeSelCoursePeriod():
    '''changes the initial course selection period
    -used by admins
    '''

    global SelCourseStart
    global SelCourseEnd

    if request.method == "POST":
        newDate = request.form["SelCourseStart"]
        newDate1 = request.form["SelCourseEnd"]
        isValidDate1 = True
        isValidDate2 = True
        isChanged_S=isChanged_E=False
        temp = SelCourseStart.strftime("%m/%d/%Y")
        temp2 = SelCourseEnd.strftime("%m/%d/%Y")

        if (newDate == '' and newDate1 == ''):       #没有输入
            isValidDate1=False
            isValidDate2=False
            flash ("失败！没有输入。 请输入时间！格式为： MM DD YYYY")
            #return redirect(url_for('changeSelCoursePeriod'))
        elif newDate != '':
            try :
                newDate = datetime.strptime(newDate, '%m %d %Y')
            except ValueError :
                isValidDate1 = False        #输入不合法
                flash  ("失败！输入不符合格式！格式为： MM DD YYYY")
            if isValidDate1:
                isChanged_S=True

        if newDate1 != '':
            try:
                newDate1 = datetime.strptime(newDate1, '%m %d %Y')
            except ValueError :
                isValidDate2 = False        #输入不合法
                flash  ("失败！输入不符合格式！格式为： MM DD YYYY" )
            if(isValidDate2):
                isChanged_E=True

        if(isValidDate1 and isValidDate2): #inputs so far are valid
            if (isChanged_S and isChanged_E):
                if newDate > newDate1: #开始日不可以晚于结束日
                    flash("失败！开始时间不能在结束时间之后！")
                    return render_template('SelectCourse/change_selection_time_INIT.html', user=session['user'])
                else:
                    SelCourseStart = newDate
                    SelCourseEnd = newDate1
            elif(isChanged_S):
                if newDate > SelCourseEnd:    #开始日不可以晚于结束日
                    flash("失败！开始时间不能在结束时间之后！")
                    return render_template('SelectCourse/change_selection_time_INIT.html', user=session['user'])
                else:
                    SelCourseStart = newDate
            elif(isChanged_E):
                if newDate1 < SelCourseStart: #结束日不可以早于开始日
                    flash ("失败！结束时间不能在开始时间之前")
                    return render_template('SelectCourse/change_selection_time_INIT.html', user=session['user'])
                else:
                    SelCourseEnd = newDate1

            temp = SelCourseStart.strftime("%m/%d/%Y")
            temp2 = SelCourseEnd.strftime("%m/%d/%Y")
            flash("初选时段更新成功！初选时段从 " + temp + " 到 " + temp2)
            return render_template('SelectCourse/change_selection_time_INIT.html', user=session['user']) #成功了
    return render_template('SelectCourse/change_selection_time_INIT.html',user=session['user'])

@bp.route('/changeSelCoursePeriodBE', methods = ["GET","POST"])
def changeSelCoursePeriodBE():
    '''changes by-election course selection period
    -used by admins
    '''

    global BESelCourseStart
    global BESelCourseEnd

    if request.method == "POST":
        newDate = request.form["BESelCourseStart"]
        newDate1 = request.form["BESelCourseEnd"]
        isValidDate1 = True
        isValidDate2 = True
        isChanged_S=isChanged_E=False
        temp = BESelCourseStart.strftime("%m/%d/%Y")
        temp2 = BESelCourseEnd.strftime("%m/%d/%Y")

        if (newDate == '' and newDate1 == ''):       #没有输入
            isValidDate1=False
            isValidDate2=False
            flash("失败！没有输入。 请输入时间！格式为： MM DD YYYY")

        elif newDate != '':
            try :
                newDate = datetime.strptime(newDate, '%m %d %Y')
            except ValueError :
                isValidDate1 = False        #输入不合法
                flash("失败！输入不符合格式！格式为： MM DD YYYY")
            if isValidDate1:
                isChanged_S=True

        if newDate1 != '':
            try:
                newDate1 = datetime.strptime(newDate1, '%m %d %Y')
            except ValueError :
                isValidDate2 = False        #输入不合法
                flash("失败！输入不符合格式！格式为： MM DD YYYY")
            if(isValidDate2):
                isChanged_E=True

        if(isValidDate1 and isValidDate2): #inputs so far are valid
            if (isChanged_S and isChanged_E):
                if newDate > newDate1: #开始日不可以晚于结束日
                    flash("失败！开始时间不能在结束时间之后！")
                    return render_template('SelectCourse/change_selection_time_BE.html', user=session['user'])
                else:
                    BESelCourseStart = newDate
                    BESelCourseEnd = newDate1
            elif(isChanged_S):
                if newDate > BESelCourseEnd:    #开始日不可以晚于结束日
                    flash("失败！开始时间不能在结束时间之后！")
                    return render_template('SelectCourse/change_selection_time_BE.html', user=session['user'])
                else:
                    BESelCourseStart = newDate
            elif(isChanged_E):
                if newDate1 < BESelCourseStart: #结束日不可以早于开始日
                    flash ("失败！结束时间不能在开始时间之前")
                    return render_template('SelectCourse/change_selection_time_BE.html', user=session['user'])
                else:
                    BESelCourseEnd = newDate1

            temp = BESelCourseStart.strftime("%m/%d/%Y")
            temp2 = BESelCourseEnd.strftime("%m/%d/%Y")
            flash("补选时段更新成功！补选时段从 " + temp + " 到 " + temp2)
            return render_template('SelectCourse/change_selection_time_BE.html', user=session['user']) #成功了

    return render_template('SelectCourse/change_selection_time_BE.html', user=session['user'])

# 用来显示选课时段和补选时段的起止时间
# 不需要的话可以直接删除！
# @app.route('/checkSelCourseTime')
# def check():
#     '''DEBUG function - used by admins to see  current course selection period dates'''
#
#     temp = SelCourseStart.strftime("%m/%d/%Y")
#     temp2 = SelCourseEnd.strftime("%m/%d/%Y")
#     temp3= BESelCourseStart.strftime("%m/%d/%Y")
#     temp4 = BESelCourseEnd.strftime("%m/%d/%Y")
#     print("Course Selection intital period changed to start:", temp, "end:" , temp2 )
#     print("Course Selection end period changed to start:", temp3, "end:" , temp4 )
#     return "initial start and end" + temp + temp2 +"by election start and end" + temp3 + temp4

@bp.route('/', methods=['GET'])
def index():
    session['user'] = 'student'
    session['teacher_id'] = 1
    session['student_id'] = 1
    session['admin_id'] = 1

    return render_template('sidebar.html', user=session['user'])

# '''
# db.drop_all()
# db.create_all()
#
# m1 = Major(name='软件工程')
# m2 = Major(name='数学')
# m3 = Major(name='英语')
# db.session.add_all([m1, m2, m3])
# db.session.commit()
# s1 = Student(name='小王', gender='男', major_id =1)
# s2 = Student(name='jack', gender='男', major_id =1)
# s3 = Student(name='mike', gender='男', major_id =2)
# db.session.add_all([s1, s2, s3])
# db.session.commit()
# t1 = Teacher(name='小红')
# t2 = Teacher(name='patt')
# t3 = Teacher(name='小李')
# db.session.add_all([t1, t2, t3])
# db.session.commit()
# c1 = Course(name='数学', teacher_id=1, time="21111125BD")
# c2 = Course(name='软件工程', teacher_id=1, time="21111344BD")
# c3 = Course(name='英语', teacher_id=2, time="21221125BD")
# c4 = Course(name='语文', teacher_id=3, time="21125355BD")
# db.session.add_all([c1, c2, c3, c4])
# db.session.commit()
#
# admin1 = Administrator(name='管理员')
# db.session.add_all([admin1])
# db.session.commit()
# '''
#
# if __name__ == '__main__':
#     app.run(debug=True)
