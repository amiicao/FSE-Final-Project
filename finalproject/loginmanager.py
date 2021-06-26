from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g
from flask_login import LoginManager
import configs
from configs import Config
login_manager = LoginManager()

def get_loginmanager():
    if 'loginmanager' not in g or g.loginmanager != login_manager:
        current_app.config.from_object(Config)
        login_manager.session_protection = 'strong'
        login_manager.login_view = 'login'  # 这个是我们没有登录的时候重定向到的地方
        login_manager.init_app(current_app)
        g.loginmanager = login_manager
    return g.loginmanager