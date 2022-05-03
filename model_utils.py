from keras.models import load_model
from flask import current_app as app

global model

def instantiate_model():
    global model
    if app.config['USE_MODEL']:
        model_file = app.config['MODEL_FILE']
        model = load_model(model_file)
        print(f"Model loaded - {model_file}")
    else:
        model = ''

def get_model():
    global model
    return model
