

class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI ="mysql://root:331998ss@localhost/furniture"
    DEBUG = True
    JWT_SECRET_KEY = "qwerty1234"
    
