from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    remember_me = BooleanField('记住用户')   # “remember me”的复选框
    verify_code = StringField("验证码")
    submit = SubmitField('登录')
