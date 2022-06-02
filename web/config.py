import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    SECRET_KEY = os.environ.get("SECRET_KEY")

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") in ('True', '1', 'T', 'Y')
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") in ('True', '1', 'T', 'Y')

    SQLALCHEMY_DATABASE_URI = ""

    DEST_EMAIL_ORDERS = os.environ.get("DEST_EMAIL_ORDERS")


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = ""


ENV = os.environ.get("ENV", "dev").lower()

if ENV == "dev":
    TheConfig = DevConfig
elif ENV == "prod":
    TheConfig = ProdConfig
else:
    ENV = "dev"
    TheConfig = DevConfig
