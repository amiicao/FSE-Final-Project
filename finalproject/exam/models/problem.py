from database import db

# 题库
from models import exam_has_problem

problem_has_tag = db.Table(
    'problem_has_tag',
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.problem_id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id')),
    info={'bind_key': 'exam'}
)


class Problem(db.Model):
    __bind_key__ = 'exam'
    problem_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)  # 0, 1, 2: 判断，单选，多选
    text = db.Column(db.Text, nullable=False)
    choice_A = db.Column(db.String(200))
    choice_B = db.Column(db.String(200))
    choice_C = db.Column(db.String(200))
    choice_D = db.Column(db.String(200))
    solution = db.Column(db.String(5), nullable=False)
    adder = db.Column(db.Integer)  # 添加人
    tags = db.relationship('Tag',
                           secondary=problem_has_tag,
                           back_populates='problems')
    papers = db.relationship('Paper',
                             secondary=exam_has_problem,
                             back_populates='problems')


class Tag(db.Model):
    __bind_key__ = 'exam'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(20), unique=True, nullable=False)
    problems = db.relationship('Problem',
                               secondary=problem_has_tag,
                               back_populates='tags')

