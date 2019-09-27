class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

    DEBUG = True
    MONGODB_SETTINGS = {'DB': 'dreamteamdb'}
    USER_APP_NAME = "E-Phoenix"
    SECRET_KEY = "Thisismysecretkey123456790"
    TESTING = False
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_REQUIRE_RETYPE_PASSWORD = False
    USER_EMAIL_SENDER_EMAIL = False
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = 'aronique@gmail.com'
    MAIL_PASSWORD = 'Carter29094964@'
    MAIL_DEFAULT_SENDER = 'aronique@gmail.com'
    MAIL_MAX_EMAILS = None
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SECRET_KEY = "Thisismysecretkey123456790"


class ProductionConfig(Config):
    """
    Production configurations
    """
    SECRET_KEY = "Thisismysecretkey123456790"

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    # 'production': ProductionConfig
}
