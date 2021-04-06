import  os
from typing import List, Type


class BaseConfig(object):
    CONFIG_NAME = 'base'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URI = 'sqlite:///data.db'
    SQLITE_DB_FILE_NAME = 'data.db'
    

class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = 'dev'
    SECRET_KEY = os.getenv('DEV_SECRET_KEY', "It's secret don't tell anyone.")
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = BaseConfig.DATABASE_URI


class TestingConfig(BaseConfig):
    CONFIG_NAME = 'test'
    SECRET_KEY = os.getenv('TEST_SECRET_KEY', "I told you not to tell anyone. I am disappointed in you.")
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',BaseConfig.DATABASE_URI)


class ProductionConfig(BaseConfig):
    CONFIG_NAME = 'prod'
    SECRET_KEY = os.getenv('PROD_SECRET_KEY', "This is your last chance. Don't tell anyone about this.")
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',BaseConfig.DATABASE_URI)


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig
]

config_by_name = {config.CONFIG_NAME: config for config in EXPORT_CONFIGS}