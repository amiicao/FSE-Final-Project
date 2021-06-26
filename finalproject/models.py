# 建立数据库table相应的类

from flask import g
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from database import db


#
# class User(db.Model):
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


class Teacher(db.Model):
    __bind_key__ = 'course_arrangement_system'
    __tablename__ = 'teacher'
    teacher_name = db.Column(db.String(45))
    teacher_id = db.Column(db.String(10), primary_key=True)

    def __repr__(self):
        return '<teacher>{}:{}'.format(self.teacher_name, self.teacher_id)


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


#
# class TermCourse(db.Model):
#     __tablename__ = 'term_course'
#     course_id = db.Column(db.String(45))
#     teacher_id = db.Column(db.String(45), primary_key=True)
#     teacher_name = db.Column(db.String(45))
#     time_code = db.Column(db.String(10), primary_key=True)
#     room_code = db.Column(db.String(6))
#
#     def __repr__(self):
#         return '<term_course>{}:{}:{}:{}:{}:{}'.format(self.course_id, self.teacher_id, self.teacher_name,
#                                                        self.time_code, self.room_code)


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


class Application(db.Model):
    __bind_key__ = 'course_arrangement_system'
    __tablename__ = 'application'
    teacher_id = db.Column(db.String(45), primary_key=True)
    content = db.Column(db.UnicodeText, primary_key=True)
    # 0:未处理 1：处理完成 2：被拒绝
    statecode = db.Column(db.SMALLINT)
    handler = db.Column(db.String(45))

    def __repr__(self):
        return '<application>{}:{}:{}:{}'.format(self.teacher_id, self.content, self.is_processed, self.handler)


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
    capacity = db.Column(db.Integer)
    instructor = db.Column(db.String(45))
    type = db.Column(db.String(20))
    time = db.Column(db.String(45))
    classroom = db.Column(db.String(45))
    description = db.Column(db.String(255))

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




class Student(db.Model):
    __bind_key__ = 'select_course'
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)    #主键
    name = db.Column(db.String(16), unique=True)
    gender = db.Column(db.Enum("男", "女"), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    courses = db.relationship("Course", secondary="student_to_course", backref="students")
    applications = db.relationship("Course", secondary="application", backref="astudents")

class StudentToCourse(db.Model):
    __bind_key__ = 'select_course'
    __tablename__ = 'student_to_course'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))

class Course_3(db.Model):
    __bind_key__ = 'select_course'
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    time = db.Column(db.String(10), nullable=False)
    curr_capacity = db.Column(db.Integer, default=0)
    max_capacity = db.Column(db.Integer, default=60)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

class BEApplication(db.Model):      #student's application for by-election
    __bind_key__ = 'select_course'
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))

class Teacher_3(db.Model):
    __bind_key__ = 'select_course'
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    courses = relationship('Course', backref='teacher')

class Major(db.Model):
    __bind_key__ = 'select_course'
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    students = db.relationship("Student", backref="major")
