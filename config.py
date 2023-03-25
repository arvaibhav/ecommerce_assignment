from datetime import timedelta

DB = "sqlite:///data.db"


class Config(object):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_SECRET_KEY = "secretKey"
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class DevConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
