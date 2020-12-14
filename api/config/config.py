class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/sample"
    UPLOAD_FOLDER = (
        "/Volumes/DATA/Learning/Flask/BuildingRESTAPIsWithFlask/Learn-Flask/images/"
    )
    # key
    SECRET_KEY = "SECRET-KEY"
    SECURITY_PASSWORD_SALT = "SECRET-KEY-PASSWORD"
    # email
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "vandong9@gmail.com"
    MAIL_PASSWORD = "honey_241105"
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/sample"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER = (
        "/Volumes/DATA/Learning/Flask/BuildingRESTAPIsWithFlask/Learn-Flask/images/"
    )
    # key
    SECRET_KEY = "SECRET-KEY"
    SECURITY_PASSWORD_SALT = "SECRET-KEY-PASSWORD"

    # email
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "vandong9@gmail.com"
    MAIL_PASSWORD = "honey_241105"
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/sample"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER = (
        "/Volumes/DATA/Learning/Flask/BuildingRESTAPIsWithFlask/Learn-Flask/images/"
    )
    # key
    SECRET_KEY = "SECRET-KEY"
    SECURITY_PASSWORD_SALT = "SECRET-KEY-PASSWORD"

    # email
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "vandong9@gmail.com"
    MAIL_PASSWORD = "honey_241105"
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False


allowed_extensions = set(["image/jpeg", "image/png", "jpeg"])


def allowed_file(filetype):
    return filetype in allowed_extensions
