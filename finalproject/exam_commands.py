"""
关于在线测试子系统的一些命令。
使用示例：
python exam_commands.py initdb --drop
python exam_commands.py forge-problems
"""

from main import create_app
from exam.models.problem import Problem, Tag
from exam.models.exam import Paper
from flask.cli import FlaskGroup
from database import db
import click


cli = FlaskGroup(create_app=create_app)


# 注册命令 initdb
@cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all(bind='exam')
    db.create_all(bind='exam')
    click.echo('Initialize database.')


# 注册命令 forge-problems
@cli.command()
@click.option('--count', default=108, help='Quantity of problems, default is 108.')
def forge_problems(count):
    """Generate fake problems."""
    from faker import Faker
    import random
    from models import User

    click.echo('Working...')

    fake = Faker('zh_CN')
    subjects = ['FDS', 'Java', '高级数据结构', '软件工程基础', '面向对象程序设计', 'C语言']
    ans = [
        ['T', 'F'],
        ['A', 'B', 'C', 'D'],
        ['A', 'B', 'C', 'D', 'AB', 'BC', 'CD', 'AC', 'BD', 'AD', 'ABC', 'ABD', 'ACD', 'BCD', 'ABCD']
    ]
    adders = User.query.filter(User.status.in_(['教师', '管理员'])).all()

    for i in range(count):
        type_index = random.randint(0, 2)
        answer = random.choice(ans[type_index])
        adder = random.choice(adders)
        problem = Problem(
            type=type_index,
            text=fake.paragraph(nb_sentences=2, variable_nb_sentences=True),
            choice_A=fake.sentence(),
            choice_B=fake.sentence(),
            choice_C=fake.sentence(),
            choice_D=fake.sentence(),
            solution=answer,
            adder=adder.uid
        )
        db.session.add(problem)
        tag_name = random.choice(subjects)
        tag = Tag.query.filter_by(tag_name=tag_name).first()
        if tag is None:
            tag = Tag(tag_name=tag_name)
        problem.tags.append(tag)

    db.session.commit()
    click.echo('Created %d fake problems.' % count)


# 注册命令 forge-papers
@cli.command()
@click.option('--count', default=10, help='Quantity of papers, default is 10.')
@click.option('--min-problem', default=5, help='Minimum number of problems in each paper, default is 5.')
def forge_papers(count, min_problem):
    """Generate fake exams."""
    from faker import Faker
    import random
    from datetime import datetime, timedelta

    click.echo('Working...')

    fake = Faker('zh_CN')
    subjects = ['FDS', 'Java', '高级数据结构', '软件工程基础', '面向对象程序设计', 'C语言']

    for i in range(count):

        name = fake.sentence(nb_words=3)
        delta = random.randint(-4, 1)
        subject = random.choice(subjects)
        strt_t = datetime.now() + timedelta(hours=delta)
        end_t = strt_t + timedelta(hours=2)

        all_problems = Problem.query.all()
        problem_count = min(random.randint(min_problem, min_problem + 20), len(all_problems))
        problems = random.sample(all_problems, k=problem_count)

        paper = Paper(
            name=name,
            subject=subject,
            strt_t=strt_t,
            end_t=end_t
        )
        db.session.add(paper)
        for problem in problems:
            paper.problems.append(problem)

    db.session.commit()
    click.echo('Created %d fake papers.' % count)


if __name__ == '__main__':
    cli()