# 建立数据库table相应的类

from flask import g
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, DateTime
from flask_sqlalchemy import SQLAlchemy
from database import db


class Teacher(db.Model):
    __tablename__ = 'teacher'
    teacher_name = db.Column(db.String(45))
    teacher_id = db.Column(db.String(10), primary_key=True)

    def __repr__(self):
        return '<teacher>{}:{}'.format(self.teacher_name, self.teacher_id)


class TermCourse(db.Model):
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
    __tablename__ = 'edu_resource'
    location = db.Column(db.String(45), primary_key=True)
    campus = db.Column(db.String(10))
    capacity = db.Column(db.Integer)
    id = db.Column(db.String(10),primary_key=True)
    status = db.Column(db.Integer)
    def __repr__(self):
        return '<edu_resource>{}:{}:{}:{}:{}'.format(self.location, self.campus, self.capacity, self.id, self.status)


class Application(db.Model):
    __tablename__ = 'application'
    teacher_id = db.Column(db.String(45), primary_key=True)
    content = db.Column(db.UnicodeText, primary_key=True)
    # 0:未处理 1：处理完成 2：被拒绝
    statecode = db.Column(db.SMALLINT)
    handler = db.Column(db.String(45))

    def __repr__(self):
        return '<application>{}:{}:{}:{}'.format(self.teacher_id, self.content, self.is_processed, self.handler)
# class Books(db.Model):
#     __tablename__ = 'books's
#     bookno = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(45))
#     title = db.Column(db.String(45))
#     price = db.Column(db.Float)
#     year = db.Column(db.Integer)
#     author = db.Column(db.String(45))
#     total = db.Column(db.Integer)
#     stock = db.Column(db.Integer)
#     press = db.Column(db.String(45))
#
#     def __repr__(self):
#         return '<Books>{}:{}:{}:{}:{}:{}:{}:{}'.format(self.bookno, self.category, self.title, self.price, self.year,
#                                                        self.author, self.total, self.stock, self.press)
#
#
# class BorrowTable(db.Model):
#     __tablename__ = 'borrowtable'
#     name = db.Column(db.String(45), db.ForeignKey('users.name'), primary_key=True, )
#     bookname = db.Column(db.String(45))
#     bno = db.Column(db.Integer, db.ForeignKey('books.bookno'), primary_key=True,)
#     borrow_time = db.Column(db.DateTime, primary_key=True)
#     return_time = Column(db.DateTime)
#     def __repr__(self):
#         return '<BorrowTable>{}:{}:{}:{}'.format(self.name, self.bookname, self.bno, self.borrow_time, self.return_time)
#
#
# class Users(db.Model):
#     __tablename__ = 'users'
#     name = db.Column(db.String(45), primary_key=True)
#     password = db.Column(db.String(300))
#     kind = db.Column(db.String(45))
#
#     def __repr__(self):
#         return '<Users>{}:{}:{}'.format(self.name, self.password, self.kind)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % self.username
