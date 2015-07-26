import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_DATABASE_URI = "postgresql://ecsuser:123456@127.0.0.1/cpa"


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s (%(asctime)s) '
                      '%(name)s: %(message)s ',
            'datefmt': "%d.%b.%Y %H:%M:%S",

        },
        'json': {
            'format': '{ "loggerName":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "lineNo":"%(lineno)d", "levelName":"%(levelname)s", "message":"%(message)s"}',
            'datefmt': "%d.%b.%Y %H:%M:%S"
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'loggly': {
            'level': 'INFO',
            'class': 'loggly.handlers.HTTPSHandler',
            'url': 'https://logs-01.loggly.com/inputs/6bb290da-13b6-401e-a101-ca9629360340/tag/cpa',
            'formatter': 'json'
        }
    },
    'loggers': {
        'cpa': {
            'handlers': ['loggly'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}