import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    SECRET_KEY = "jkas90d3jw2e9qwndjklaq09wdasjlnkdasidadASKDASD321"

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") in ('True', '1', 'T', 'Y')
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") in ('True', '1', 'T', 'Y')
