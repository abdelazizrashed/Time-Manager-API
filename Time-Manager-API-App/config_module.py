import  os


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///data.db'
    sqlite_db_name = 'data.db'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DATABASE_URI = os.environ.get('DATABASE_URL', Config.DATABASE_URI)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True