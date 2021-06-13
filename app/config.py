import os
from datetime import timedelta
from typing import List, Type
import string


def get_db_url_modifies(default):
    url = os.environ.get("DATABASE_URL", default)
    if url != default:
        url = url.replace("postgres", "postgresql", 1)
    return url


class BaseConfig(object):
    CONFIG_NAME = "base"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URI = "sqlite:///data.db"
    SQLITE_DB_FILE_NAME = "data.db"
    JWT_SECRET_KEY = "secret key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    SECRET_KEY = os.getenv("DEV_SECRET_KEY", "It's secret don't tell anyone.")
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_db_url_modifies(BaseConfig.DATABASE_URI)
    JWT_SECRET_KEY = "secret key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.getenv(
        "TEST_SECRET_KEY", "I told you not to tell anyone. I am disappointed in you."
    )
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_db_url_modifies(BaseConfig.DATABASE_URI)
    JWT_SECRET_KEY = "secret key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    SECRET_KEY = os.getenv(
        "PROD_SECRET_KEY", "This is your last chance. Don't tell anyone about this."
    )
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_db_url_modifies(BaseConfig.DATABASE_URI)
    JWT_SECRET_KEY = "secret key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    PROPAGATE_EXCEPTIONS = True


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]

config_by_name = {config.CONFIG_NAME: config for config in EXPORT_CONFIGS}
