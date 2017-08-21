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
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_RESULT_BACKEND = 'amqp://deploy:deploy@localhost:5672/aha'
    CELERY_BROKER_URL = 'amqp://deploy:deploy@localhost:5672/aha'
    SESSION_TYPE = 'sqlalchemy'
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_SALT = "supersecret"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'wsu.aha@gmail.com'
    MAIL_PASSWORD = 'aha@wsu#17'
    SECURITY_CHANGABLE = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host:5432/aha'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True


config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,
  'testing': TestingConfig,
  'default': DevelopmentConfig
}
