from flask import Flask
import logging
from logging import Formatter, FileHandler

# extensions
from flask_bootstrap import Bootstrap
from routes import routes
from model_utils import instantiate_model

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
        
    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app

def register_extensions(app):
    """Register all Extensions
    This registers all the add-ons of the app,
    to be instantiated with the instance of the flask app
    Add your extensions to this functions e.g Mail

    :param app: Flask app instance
    :return: None
    :rtype: NoneType
    """

    routes(app)
    bootstrap = Bootstrap(app)
    with app.app_context():
        global model
        instantiate_model()
