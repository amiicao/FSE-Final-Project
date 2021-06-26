# 数据库配置
HOST = 'rm-2zeb626gl3ajx1372ho.mysql.rds.aliyuncs.com'
PORT = '3306'
# 数据库名
DATABASE = 'course_arrangement_system'
USERNAME = 'fse_g7'
PASSWORD = 'FSE_group7'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                        password=PASSWORD, host=HOST,
                                                                                        port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
