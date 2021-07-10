# 建立数据库table相应的类
from datetime import datetime

from flask import g
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from database import db


# class Teacher(db.Model):
#     __bind_key__ = 'course_arrangement_system'
#     __tablename__ = 'teacherinclassarrange'
#     teacher_name = db.Column(db.String(45))
#     teacher_id = db.Column(db.Integer,db.ForeignKey('user.uid',ondelete='CASCADE'),primary_key=True)
#
#     def __repr__(self):
#         return '<teacher>{}:{}'.format(self.teacher_name, self.teacher_id)

class Teacher(db.Model):
    __bind_key__ = 'message_management_system'
    __tablename__ = 'teacher'
    name = db.Column(db.String(45))
    id = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    courses = relationship('Course', backref='teacher')

    def __repr__(self):
        return '<teacher>{}:{}'.format(self.name, self.id)

class TermCourse(db.Model):
    __bind_key__ = 'course_arrangement_system'
    __tablename__ = 'term_course'
    course_id = db.Column(db.String(10), primary_key=True)
    teacher_id = db.Column(db.String(10), primary_key=True)
    course_name = db.Column(db.String(45))
    time = db.Column(db.String(14))
    credit = db.Column(db.Integer)

    def __repr__(self):
        return '<term_course>{}:{}:{}:{}'.format(self.course_id, self.teacher_id, self.course_name,
                                                 self.time, self.credit)


class Classroom(db.Model):
    __bind_key__ = 'course_arrangement_system'
    __tablename__ = 'edu_resource'
    location = db.Column(db.String(45), primary_key=True)
    campus = db.Column(db.String(10))
    capacity = db.Column(db.Integer)
    id = db.Column(db.String(10), primary_key=True)
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<edu_resource>{}:{}:{}:{}:{}'.format(self.location, self.campus, self.capacity, self.id, self.status)


class ModifyApplication(db.Model):
    __bind_key__ = 'course_arrangement_system'
    __tablename__ = 'modifyapplication'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    teacher_id = db.Column(db.Integer,db.ForeignKey('teacherinclassarrange.teacher_id',ondelete='CASCADE'), primary_key=True)
    content = db.Column(db.UnicodeText, primary_key=True)
    # 0:未处理 1：处理完成 2：被拒绝
    statecode = db.Column(db.SMALLINT)
    handler = db.Column(db.String(45))

    def __repr__(self):
        return '<application>{}:{}:{}:{}'.format(self.teacher_id, self.content, self.statecode, self.handler)


# class User(db.Model):
#     __bind_key__ = 'message_management_system'
#     __tablename__ = 'user'
#     uid = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(45))
#     sex = db.Column(db.String(25))
#     age = db.Column(db.Integer)
#     status = db.Column(db.String(45))
#     password = db.Column(db.String(45))
#     def __repr__(self):
#         return '<user>{}:{}:{}:{}:{}:{}'.format(self.uid,self.name,self.sex,self.age,self.status,self.password)

class Course(db.Model):
    __bind_key__ = 'message_management_system'
    __tablename__ = 'course'
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    credit = db.Column(db.Integer)
    curr_capacity = db.Column(db.Integer, default=0)
    capacity = db.Column(db.Integer, default=60)
    instructor = db.Column(db.String(45))
    type = db.Column(db.String(20))
    time = db.Column(db.String(14))
    classroom = db.Column(db.String(45))
    description = db.Column(db.String(255))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return '<course>{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.cid, self.name, self.credit, self.capacity,
                                                           self.instructor, self.type, self.time, self.classroom,
                                                           self.description)


# 以下是对于用户类(仅仅提供给登录用)的创立
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __bind_key__ = 'message_management_system'
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    sex = db.Column(db.String(25))
    age = db.Column(db.Integer)
    status = db.Column(db.String(45))
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<user>{}:{}:{}:{}:{}:{}'.format(self.uid, self.name, self.sex, self.age, self.status, self.password)

    # 打印自己的uid
    def __repr__(self):
        return '<User {}>'.format(self.uid)

    # (未详细设计)这个需要返回的是用户在session中的唯一编号
    def get_id(self):
        return self.uid

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# StudentToCourse = db.Table(
#     'student_to_course',
#     db.Column('id',db.Integer,primary_key=True),
#     db.Column('student_id',db.Integer, db.ForeignKey("student.id")),
#     db.Column('course_id',db.Integer, db.ForeignKey("course.cid"))
# )

class Student(db.Model):
    __bind_key__ = 'message_management_system'
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(16), unique=True)
    gender = db.Column(db.Enum("男", "女"), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    courses = db.relationship("Course", secondary='student_to_course', backref="students")
    applications = db.relationship("Course", secondary="application", backref="astudents")


class StudentToCourse(db.Model):
    __bind_key__ = 'message_management_system'
    __tablename__ = 'student_to_course'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.cid"))


class BEApplication(db.Model):  # student's application for by-election
    __bind_key__ = 'message_management_system'
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.cid"))


# class Teacher_3(db.Model):
#     __bind_key__ = 'select_course'
#     __tablename__ = 'teacher'
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(16), unique=True)
#     courses = relationship('Course', backref='teacher_3')


class Major(db.Model):
    __bind_key__ = 'select_course'
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    # students = db.relationship("Student", backref="major")


############################################## G_9 exam
exam_has_problem = db.Table(
    'exam_has_problem',
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.problem_id')),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.paper_id')),
    info={'bind_key': 'exam'}
)


class Paper(db.Model):
    __bind_key__ = 'exam'
    name = db.Column(db.String(50), nullable=False)
    paper_id = db.Column(db.Integer, primary_key=True, nullable=False)
    subject = db.Column(db.String(40), nullable=False)
    strt_t = db.Column(db.DateTime, default=datetime.now, nullable=False)
    end_t = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.Boolean, default=False)  # 是否已经结束
    score = db.Column(db.Float, default=-1)  # 平均分
    anlsflag = db.Column(db.Boolean, default=False)  # 是否已经分析
    problems = db.relationship('Problem',
                               secondary=exam_has_problem,
                               back_populates='papers')
    anspapers = db.relationship("Anspaper", lazy='dynamic')
    probanls = db.relationship('ProbAnalysis')
    to_class = db.Column(db.Integer, db.ForeignKey('course.cid', ondelete='CASCADE'), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacherinclassarrange.teacher_id'), nullable=True)


class Resource(db.Model):
    __tablename__ = 'resource'
    res_id = db.Column(db.String(10), primary_key=True)
    res_name = db.Column(db.String(45))
    provider_id = db.Column(db.String(10), primary_key=True)
    provider_type = db.Column(db.String(1), primary_key=True)
    res = db.Column(db.LargeBinary)
    upload_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<resource>{}:{}:{}:{}:{}:{}'.format(self.res_id, self.res_name, self.provider_id,
                                                    self.provider_type, self.res, self.upload_date)


class Score(db.Model):
    __tablename__ = 'score'
    stu_id = db.Column(db.String(10), primary_key=True)
    course_id = db.Column(db.String(10), primary_key=True)
    score_total = db.Column(db.Float(4, 1))
    score_general = db.Column(db.Float(4, 1))
    score_final = db.Column(db.Float(4, 1))

    def __repr__(self):
        return '<score>{}:{}:{}:{}:{}'.format(self.stu_id, self.course_id, self.score_total,
                                              self.score_general, self.score_final)


class CourseHomework(db.Model):
    __tablename__ = 'course_homework'
    course_id = db.Column(db.String(10), primary_key=True)
    hm_seq = db.Column(db.String(10), primary_key=True)

    def __repr__(self):
        return '<course_homework>{}:{}'.format(self.course_id, self.hm_seq)


class Homework(db.Model):  # not sure if it should be db.Model
    __tablename__ = 'homework'
    hm_seq = db.Column(db.String(10), primary_key=True)
    hm_title = db.Column(db.String(45))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<homework>{}:{}:{}:{}'.format(self.hm_seq, self.hm_title,
                                              self.start_date, self.end_date)


class StudentHomework(db.Model):
    __tablename__ = 'stu_homework'
    stu_id = db.Column(db.String(10), primary_key=True)  # db.ForeignKey(student.id)
    hm_seq = db.Column(db.String(10), primary_key=True)

    def __repr__(self):
        return '<stu_homework>{}:{}'.format(self.stu_id, self.hm_seq)
