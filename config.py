#encoding: utf-8

# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'test'
PASSWORD = 'test123'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'flaskDB'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# os.urandom(24)
SECRET_KEY = b'\xf9\xcb!v3\xbf\x06\x01\xcd\xa7rVL\xb8\x1dH0\x15!d\xa1\xa7\xe0\xca'
