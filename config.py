class Configuration(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///itprotection.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "2281488"
    CACHE_TYPE = "null"
    SECURITY_PASSWORD_SALT = "salt"
    SECURITY_PASSWORD_HASH = "bcrypt"
