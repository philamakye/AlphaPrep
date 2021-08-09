import os

class BaseConfig(object):
    DEBUG = False
    
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = 'development'
    SECRET_KEY = os.environ['ALPHA_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['ALPHA_NEW_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
    
    MAIL_SERVER = 'smtp.gmail.com'      # using google's mail service
    MAIL_PORT = 465 # well this is the mail port
    MAIL_USE_TL = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['ALPHA_MAIL']
    MAIL_PASSWORD = os.environ['ALPHA_MAIL_PASSWORD']    
    
    MYSQL_DATABASE_USER = os.environ['ALPHA_DB_USER']
    MYSQL_DATABASE_PASSWORD = os.environ['ALPHA_DB_PASSWORD']
    MYSQL_DATABASE_DB = os.environ['ALPHA_DB_NAME']
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_AUTH_PLUGIN='mysql_native_password'
    
    
class TestingConfig(BaseConfig):
    DEBUG = True
    
    

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "production_database_uri"



    