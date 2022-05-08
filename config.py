from dotenv import load_dotenv
import os
from distutils.util import strtobool

load_dotenv()


class Config(object):
    """Config base class
    This is the default configuration class for your app. You should
    `probably` not use this directly, instead extend this class with
     your custom config for different environments
    """
    DEBUG = False
    TESTING = False
    ENV = 'development'
    UPLOAD_PATH = 'static/uploads/'
    IMAGE_SIZE = 200
    MAX_CONTENT_LENGTH = 4 * 2048 * 2048
    UPLOAD_EXTENSIONS = ['.jpg', '.png']
    USE_MODEL = strtobool(os.getenv('USE_MODEL', 'True'))

    CATEGORIES = []


class DevelopmentConfig(Config):
    """Development Config
    This extends the `Config` base class to store variables
    for development environments
    """
    DEBUG = True
    FLASK_APP = 'APP-DEV'
    SECRET_KEY = os.getenv('SECRET_KEY')
    PORT = os.getenv('PORT', 8000)
    USE_MODEL = strtobool(os.getenv('USE_MODEL', 'True'))
    MODEL_FILE = 'model_v_1'
    CATEGORIES = [
        'cardboard',
        'glass',
        'metal',
        'paper',
        'plastic',
        'trash'
    ]


class TestingConfig(Config):
    """Testing Config
       This extends the `Config` base class to store variables
       for testing environments
       """
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class StagingConfig(Config):
    """Staging Config
       This extends the `Config` base class to store variables
       for staging environments

       """
    pass


class ProductionConfig(Config):
    """Production Config
       This extends the `Config` base class to store variables
       for production environments

       """
    ENV = 'production'
    DEBUG = False
    FLASK_APP = 'APP-DEV'
    SECRET_KEY = os.getenv('SECRET_KEY')
    PORT = os.getenv('PORT', 8000)
    USE_MODEL = strtobool(os.getenv('USE_MODEL', 'True'))
    MODEL_FILE = 'model_v_1'
    CATEGORIES = [
        'cardboard',
        'glass',
        'metal',
        'paper',
        'plastic',
        'trash'
    ]
