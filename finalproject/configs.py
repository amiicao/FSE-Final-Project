# 数据库配置
import os

HOST = 'rm-2zeb626gl3ajx1372ho.mysql.rds.aliyuncs.com'
PORT = '3306'
# 数据库名
DATABASE1 = 'message_management_system'
DATABASE2 = 'course_arrangement_system'
DATABASE3 = 'select_course'
USERNAME = 'fse_g7'
PASSWORD = 'FSE_group7'


DB_URI_I = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                        password=PASSWORD, host=HOST,
                                                                                        port=PORT, db=DATABASE1)

DB_URI_II = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                        password=PASSWORD, host=HOST,
                                                                                        port=PORT, db=DATABASE2)

DB_URI_III = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                        password=PASSWORD, host=HOST,
                                                                                        port=PORT, db=DATABASE3)
SQLALCHEMY_DATABASE_URI = DB_URI_I
SQLALCHEMY_BINDS = {
    'course_arrangement_system':        DB_URI_II,
    'message_management_system':        DB_URI_I,
    'select_course':                    DB_URI_III
}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # 数据库配置
    HOST = 'rm-2zeb626gl3ajx1372ho.mysql.rds.aliyuncs.com'
    PORT = '3306'
    # 数据库名
    DATABASE = 'message_management_system'
    USERNAME = 'fse_g7'
    PASSWORD = 'FSE_group7'

    DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                            password=PASSWORD, host=HOST,
                                                                                            port=PORT, db=DATABASE)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
