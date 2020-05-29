""" Setting up configurations for the FLASK app """


class BaseConfig():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///my_db.db"
    SECRET_KEY = b'}qe\x9e\xb7P\x8f~l;N\xff\xf8Uu\x18\x19\xdb\xc0\\'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING  = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    TESTING =  True

