from flask import Flask
import logging
import logging.config


def create_app():
    app = Flask(__name__)

    ##############
    ### config ###
    ##############
    import os
    config_type = os.environ.get('CONFIG_TYPE')
    from app.config import DevelopmentConfig, ProductionConfig, TestingConfig, LOGGING
    if config_type == 'production':
        app.config.from_object(ProductionConfig)
    elif config_type == 'testing':
        LOGGING['loggers']['cpa']['handlers'] = ['console']
        app.config.from_object(TestingConfig)
    else:
        LOGGING['loggers']['cpa']['handlers'] = ['console']
        app.config.from_object(DevelopmentConfig)
    logging.config.dictConfig(LOGGING)
    return app


application = create_app()


###############
### manager ###
###############
from flask.ext.script import Manager
manager = Manager(application)


################
### database ###
################
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(application)


###############
### signals ###
###############
from . import signals


#############
### views ###
#############
from . import views


#############
### admin ###
#############
from .admin import admin


####################
### CORS headers ###
####################
from flask_cors import CORS
cors = CORS(application)


################
### REST API ###
################
from .rest_api import api