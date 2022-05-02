# Import modules from flask and werkzeug libraries

from flask import Flask, request, jsonify, render_template, flash

from werkzeug.utils import secure_filename

import numpy as np
import os


from keras.preprocessing.image import load_img

from keras.preprocessing.image import img_to_array

from keras.models import load_model

from tensorflow.keras.applications import inception_resnet_v2

from tensorflow.keras.preprocessing import image

import filetype

from PIL import Image
import io


UPLOAD_FOLDER = os.path.relpath('static/uploads')

IMAGE_SIZE = 200

CATEGORIES = [
    'cardboard',
    'glass',
    'metal',
    'paper',
    'plastic',
    'trash'
]


ALLOWED_FILE_TYPES = [
    'image/jpeg',
    'image/png'
]


model = load_model("inception_resnetv2_garbage_4.h5")

print("model loaded")


def load_image(img_path):

    img = image.load_img(img_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))

    # (height, width, channels)
    img_tensor = image.img_to_array(img)

    # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)

    # imshow expects values in the range [0, 1]
    img_tensor /= 255.
    return img_tensor


def predict_image(image):
    pred = model.predict(image)

    predictions = {CATEGORIES[i]: round(
        prediction, 2) for i, prediction in enumerate(pred[0]) if prediction > 0.2}

    return(CATEGORIES[np.argmax(pred, axis=1)[0]], predictions)


app = Flask(__name__)  # create a flask app

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'very secret indeed'

app.config['MAX_CONTENT_LENGTH'] = 2048 * 2048


@app.route('/')
def index():

    return render_template('view.html', title="Upload an Image!")


@app.route('/predict', methods=['POST'])
def predict_request():

    # Get file and save it

    if 'image_file' not in request.files:

        return 'there is no image in form!'

    uploaded_file = request.files['image_file']

    if uploaded_file.content_type in ALLOWED_FILE_TYPES:
        # filename = secure_filename(uploaded_file.filename)
        new_filename = f"process_image.{uploaded_file.content_type.replace('image/', '')}"
        path = os.path.join(app.config['UPLOAD_FOLDER'],new_filename)

        if os.path.exists(path):
            os.remove(path)

        uploaded_file.save(path)

        # Send prediction request
        image = load_image(path)
        prediction, predictions = predict_image(image)

        flash('Image processed successfully!', 'success')

        return render_template('view.html', image_prediction=prediction, user_image=path, predictions=predictions)

    else:

        flash('Unable to process that filetype', 'danger')

        return render_template('view.html', title="Upload an Image!")


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8069, debug=True)
