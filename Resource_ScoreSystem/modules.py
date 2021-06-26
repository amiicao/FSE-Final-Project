# create corresponding class of database table

from flask import g
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, DateTime, LargeBinary
from flask_sqlalchemy import SQLAlchemy
from database import db


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
    stu_id = db.Column(db.String(10), primary_key=True)   #  db.ForeignKey(student.id)
    hm_seq = db.Column(db.String(10), primary_key=True)

    def __repr__(self):
        return '<stu_homework>{}:{}'.format(self.stu_id, self.hm_seq)
