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


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    img_format = imghdr.what(None, header)
    if not img_format:
        return None
    return '.' + (img_format if img_format != 'jpeg' else 'jpg')


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
    file_path = os.path.join(
        app.config['UPLOAD_PATH'], f"{new_filename}.{file_ext}")
    uploaded_file.save(file_path)

    prediction = 'toast'
    predictions = {'toast': 50, 'vegemite':75, 'butter':30}

    if app.config['USE_MODEL']:
        image = load_image(file_path)
        prediction, predictions = predict_image(image)

    predictions = sorted(predictions.items(), key=lambda x:x[1], reverse=True)
    return jsonify(html=render_template('components/prediction_card.html', prediction=prediction, predictions=predictions, image_path=file_path))


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
