from flask import Flask, render_template, url_for, request, json,jsonify
from flask_sqlalchemy import SQLAlchemy
import configs
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.from_object(configs)
db = SQLAlchemy(app)
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

class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45))
    sex = db.Column(db.String(25))
    age = db.Column(db.Integer)
    status = db.Column(db.String(45))
    def __repr__(self):
        return '<user>{}:{}:{}:{}:{}'.format(self.uid,self.name,self.sex,self.age,self.status)

class Course(db.Model):
    __tablename__ = 'course'
    cid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(45))
    credit = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    instructor = db.Column(db.String(45))
    type = db.Column(db.String(20))
    time = db.Column(db.String(45))
    classroom = db.Column(db.String(45))
    description = db.Column(db.String(255))
    def __repr__(self):
        return '<course>{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.cid, self.name, self.credit, self.capacity, self.instructor,self.type, self.time, self.classroom, self.description)


@app.route('/personal-center.html', methods=['GET', 'POST'])
def personal_center():
    u = User(uid='123',sex='男',age='200',name='shx',status='Stu')
    return render_template("personal-center.html", user = u)

@app.route('/EditInfo', methods=['GET', 'POST'])
def EditInfo():
    uid = request.form.get('uid')
    name = request.form.get('name')
    age = request.form.get('age')
    sex = request.form.get('sex')

    print(uid,name,age,sex)

    u = User('123','男','200','shx','Stu')
    return render_template("personal-center.html", user = u)

@app.route('/course-information.html/<cid>', methods=['GET', 'POST'])
def course_information(cid):
    print(str(cid))
    #c = Course('计算机系统原理','软工十大垃圾课','4','100','12345','楼sir','工科','周二','西1-208')
    c = Course.query.filter(Course.cid==cid).first()
    return render_template("course-information.html", course = c)

@app.route('/course-search.html', methods=['GET', 'POST'])
def course_search():
    #c = [Course('1','2','3','4','5','6','7','8','9'), Course('9','8','7','6','5','4','3','2','1')]
    c = Course.query.all()
    return render_template("course-search.html", courses=c)

@app.route('/EditCourse', methods=['GET', 'POST'])
def EditCourse():
    name = request.form.get('name')
    cid = request.form.get('cid')
    time = request.form.get('time')
    classroom = request.form.get('classroom')
    instructor = request.form.get('instructor')
    credit = request.form.get('credit')
    type = request.form.get('type')
    description = request.form.get('description')
    capacity = request.form.get('capacity')

    #print(name,cid,time,classroom,instructor,credit,type)

    # c = [Course('1','2','3','4','5','6','7','8','9'), Course('9','8','7','6','5','4','3','2','1')]
    Course.query.filter((Course.cid) == cid).update({'name':name,'time':time,'classroom':classroom,'instructor':instructor,'credit':credit,'type':type, 'description':description, 'capacity':capacity})
    db.session.commit()
    c = Course.query.all()
    return render_template("course-search.html", courses=c)

@app.route('/course-delete/<cid>', methods=['GET', 'POST'])
def DeleteCourse(cid):
    delete_course = Course.query.filter(Course.cid == cid).first()
    db.session.delete(delete_course)
    db.session.commit()

    c = Course.query.all()
    return render_template("course-search.html", courses=c)

@app.route('/AddCourse', methods=['GET', 'POST'])
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

    NewCourse = Course(name=name,description=description,credit=credit,capacity=capacity,cid=cid,instructor=instructor,type=type,time=time,classroom=classroom)
    db.session.add(NewCourse)
    db.session.commit()

    c = Course.query.all()
    return render_template("course-search.html", courses=c)

@app.route('/user-search.html', methods=['GET', 'POST'])
def user_search():
    #u = [User('1','2','3','4','5'), User('5','4','3','2','1')]
    u = User.query.all()
    return render_template("user-search.html", users=u)

@app.route('/AddUser', methods=['GET', 'POST'])
def AddUser():
    uid = request.form.get('uid')
    name = request.form.get('name')
    age = request.form.get('age')
    sex = request.form.get('sex')
    status = request.form.get('status')

    print(uid,name,age,sex,status)
    
    NewUser = User(uid=uid, name=name, age=age, sex=sex, status=status)
    db.session.add(NewUser)
    db.session.commit()

    u = User.query.all()
    return render_template("user-search.html", users=u)

@app.route('/SubmitPhoto', methods=['GET', 'POST'])
def SubmitPhoto():
    photo = request.files['photo']
    u = User(uid='123',sex='男',age='200',name='shx',status='Stu')
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = basedir + "\\static\\assets\\images\\lg\\" + u.uid + '.jpg'
    photo.save(file_path) 
    return render_template("personal-center.html", user=u)

'''
@app.route('/')
def hello_world():
    user1 = User(uid=100,sex='nan',age=10,status="sss",name='lou')
    db.session.add(user1)
    db.session.commit()
    return 'Hello World!'
'''
if __name__ == '__main__':

    app.run()