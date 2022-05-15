from flask import render_template, current_app as app, request, url_for, flash, abort, make_response, jsonify
import numpy as np
from tensorflow.keras.preprocessing import image
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from PIL import Image
from tensorflow.keras.applications import inception_resnet_v2
import imghdr
from werkzeug.utils import secure_filename
import os
import uuid
from model_utils import get_model
from suggestions import Suggestions

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    img_format = imghdr.what(None, header)
    if not img_format:
        return None
    return '.' + (img_format if img_format != 'jpeg' else 'jpg')


def report_model_prediction():
    json_data = request.get_json()

    if not 'correct' in json_data or not 'filepath' in json_data:
        abort(400)

    filename = os.path.split(json_data['filepath'])[-1]
    new_filepath = os.path.join(f'static/reported_images/{"good" if json_data["correct"] else "bad"}', filename)
    potential_filepath = os.path.join(f'static/reported_images/{"bad" if json_data["correct"] else "good"}', filename)
        
    if not os.path.exists(new_filepath) and not os.path.exists(potential_filepath):
        os.rename(json_data['filepath'], new_filepath)

        return make_response(jsonify(msg='Thank you for the feedback'), 200)

    return make_response(jsonify(msg='You have already given feedback for this image'), 200)

# ajax route for uploading a file and returning model predictions
def make_prediction():
    if 'image_file' not in request.files or not request.files['image_file']:
        abort(400)

    uploaded_file = request.files['image_file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext.lower() != validate_image(uploaded_file.stream):
            abort(400)

    new_filename = str(uuid.uuid4())
    file_path = app.config['UPLOAD_PATH'] + new_filename + file_ext
    uploaded_file.save(file_path)

    prediction = 'toast'
    predictions = {'toast': 50, 'vegemite':75, 'butter':30}

    if app.config['USE_MODEL']:
        image = load_image(file_path)
        prediction, predictions = predict_image(image)

    text, link = get_suggestions(prediction)

    predictions = sorted(predictions.items(), key=lambda x:x[1], reverse=True)
    return jsonify(html=render_template('components/prediction_card.html', predictions=predictions, image_path=file_path, text=text, link=link))


def load_image(img_path):
    image_size = app.config['IMAGE_SIZE']
    img = image.load_img(img_path, target_size=(image_size, image_size))

    # (height, width, channels)
    img_tensor = image.img_to_array(img)

    # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)

    # imshow expects values in the range [0, 1]
    img_tensor /= 255.
    return img_tensor


def predict_image(image):
    model = get_model()
    categories = app.config['CATEGORIES']
    pred = model.predict(image)
    predictions = {
        categories[i]: int(prediction*100) for i, prediction in enumerate(pred[0]) if prediction > 0.2
    }
    return(categories[np.argmax(pred, axis=1)[0]], predictions)

def get_suggestions(image_class):
    switch = {
        'cardboard':Suggestions.cardboard(),
        'e-waste':Suggestions.ewaste(),
        'glass':Suggestions.glass(),
        'metal':Suggestions.metal(),
        'paper':Suggestions.paper(),
        'plastic':Suggestions.plastic(),
        'trash':Suggestions.trash()
    }

    return switch[image_class]