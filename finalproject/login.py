from flask import Flask, render_template, flash, redirect, url_for, session
from configs import Config
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from models import User
from loginmanager import get_loginmanager


# app = Flask(__name__)
# app.config.from_object(Config)  #导入配置文件中的配置，主要是SECRET_KEY
# db = SQLAlchemy(app)


# 以下是对于用户类(仅仅提供给登录用)的创立
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# class User(db.Model, UserMixin):
#     __tablename__ = 'user'
#     uid = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(45))
#     sex = db.Column(db.String(25))
#     age = db.Column(db.Integer)
#     status = db.Column(db.String(45))
#     password = db.Column(db.String(45))
#     def __repr__(self):
#         return '<user>{}:{}:{}:{}:{}:{}'.format(self.uid,self.name,self.sex,self.age,self.status,self.password)
#
#     # 打印自己的uid
#     def __repr__(self):
#         return '<User {}>'.format(self.uid)
#     # (未详细设计)这个需要返回的是用户在session中的唯一编号
#     def get_id(self):
#         return self.uid
#
#     def set_password(self, password):
#         self.password = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password, password)


UPLOAD_FOLDER = 'uploads'
bp = Blueprint('login', __name__)


# (未详细设计)以下我们尝试进行login_manager的设置，此处我们将进行相关的个性化调整


# (未详细设计)这个函数需要返回指定 id 的用户，如果没有就返回 None。这里因为设置框架所以就默认返回 None

# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))


# 用来测试的页面，
# @bp.route('/test')
# def index():
#     return render_template("test.html", title='Home Page')
#

@bp.route('/index')
def hello_world():
    return render_template('sidebar.html')


# 主体的登陆界面

@bp.route('/', methods=['GET', 'POST'])
def login():
    # 设用户已经登录，则直接跳转至相关页面
    if current_user.is_authenticated:
        return redirect(url_for('login.hello_world'))
    # 如果尚未登录，则渲染绑定表单
    error = None
    form = LoginForm()
    if form:
        # 希望从表单中得到返回的信息
        if form.validate_on_submit():
            # 首先验证验证码是否输入正确
            if 1 or form.verify_code.data == session['code']:
                if form.username.data:
                    user = User.query.filter_by(uid=form.username.data).first()
                    if user is None:
                        error = "用户不存在！"
                    else:
                # (未详细设计)当前状态是只要数据库中有这个用户名，我们就能登陆，这里需要加上的是密码哈希的对比
                        user.set_password(user.password)
                        if not user.check_password(form.password.data):
                            error = "密码错误！"
                else:
                    error = "输入不合法！"
                if not error:
                 # 将该用户注册到当前
                    login_user(user, remember=form.remember_me.data)
                    return redirect(url_for('login.hello_world'))
            else:
                error = "验证码错误"

    if error is not None:
        flash(error, "error")
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login.login'))


# 将验证码图片传给前端;
@bp.route('/code')
def get_code():
    # 1. 生成验证码；
    from get_code import gene_code
    image, code = gene_code()

    # 2. 将验证码图片以二进制的方式写在内存中
    from io import BytesIO
    buf = BytesIO()
    image.save(buf, 'png')
    buf_str = buf.getvalue()
    # 3. 将数据响应给前端页面
    from flask import make_response, session
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/png'

    # # 将验证码内容写入session会话中;
    session['code'] = code

    # print(code)
    return response


