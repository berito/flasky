import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in [
        'true', 'on', '1']
    MAIL_USERNAME = os.environ.get(
        'MAIL_USERNAME') or 'mohammedsrajk@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'dvdnyroecwhkwhpn'
    FLASK_COVERAGE=os.environ.get('FLASK_COVERAGE')
    FLASKY_POSTS_PER_PAGE=os.environ.get('FLASKY_POSTS_PER_PAGE') or 5
    FLASKY_FOLLOWERS_PER_PAGE=os.environ.get('FLASKY_FOLLOWERS_PER_PAGE') or 5
    FLASKY_COMMENTS_PER_PAGE=os.environ.get('FLASKY_COMMENTS_PER_PAGE') or 5
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'mohammedsrajk@gmail.com'
    FLASKY_SLQW_DB_QUERY_TIME=os.environ.get('FLASKY_SLQW_DB_QUERY_TIME') or 0.5
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
    @classmethod
    def init_app(cls,app):
        config.__init__app(app)
        #email errors to the administrator
        import logging
        from logging.handlers import SMTPHandler
        credentials=None
        secure=None
        if getattr(cls,'MAIL_USERNAME',None) is not None:
            credentials=(cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USE_TLS',None):
                secure=()
        mail_handler = SMTPHandler(
        mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        fromaddr=cls.FLASKY_MAIL_SENDER,
        toaddrs=[cls.FLASKY_ADMIN],
        subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
        credentials=credentials,
        secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'data.sqlite')


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL') or 'sqlite://'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
