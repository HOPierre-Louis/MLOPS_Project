
"""
simple python flask application
"""
# Test 1
##########################################################################
## Imports
##########################################################################

import os
import ast

import numpy as np
import tensorflow as tf
import keras
from keras.models import load_model

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask.json import jsonify
from flask_cors import CORS

##########################################################################
## Application Setup
##########################################################################

app = Flask(__name__)
cors = CORS(app)

##########################################################################
## Model Setup
##########################################################################

loaded_model = load_model('./model/fashion_mnist_model.h5')

class_labels = {0: 'T-shirt/top',
                1: 'Trouser',
                2: 'Pullover',
                3: 'Dress',
                4: 'Coat',
                5: 'Sandal',
                6: 'Shirt',
                7: 'Sneaker',
                8: 'Bag',
                9: 'Ankle boot'}

##########################################################################
## Routes
##########################################################################

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/hello")
def hello():
    """
    Return a hello message
    """
    return jsonify({"hello": "world"})

@app.route("/api/hello/<name>")
def hello_name(name):
    """
    Return a hello message with name
    """
    return jsonify({"hello": name})

@app.route("/api/whoami")
def whoami():
    """
    Return a JSON object with the name, ip, and user agent
    """
    return jsonify(
        name=request.remote_addr,
        ip=request.remote_addr,
        useragent=request.user_agent.string
    )

@app.route("/api/whoami/<name>")
def whoami_name(name):
    """
    Return a JSON object with the name, ip, and user agent
    """
    return jsonify(
        name=name,
        ip=request.remote_addr,
        useragent=request.user_agent.string
    )

@app.route('/classify/<path:array>', methods=['GET', 'POST'])
def classify(array):
    image = ast.literal_eval(array)

    # preprocess the image
    image = np.array(image, dtype=np.float32)
    image = image.reshape(1, 28, 28, 1)
    image = image.astype("float32")
    image /= 255

    # make the prediction
    prediction = loaded_model.predict(image)
    label = int(np.argmax(prediction))
    return jsonify({"prediction": label, 'label': class_labels[label]})

##########################################################################
## Main
##########################################################################

if __name__ == '__main__':
    app.run(port= 5050, debug=True)
