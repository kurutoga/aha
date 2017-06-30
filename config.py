class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://aha:python@localhost:5432/aha'
    SECURITY_URL_PREFIX = '/auth'
    SECURITY_POST_LOGIN_VIEW = '/dashboard'
    SECURITY_POST_REGISTER_VIEW = '/dashboard'
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'secret'
    SECRET_KEY = 'supersecret'
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host:5432/aha'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
