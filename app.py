
"""
simple python flask application
"""

##########################################################################
## Imports
##########################################################################

import os
import ast
import pickle
import nltk
import json

import numpy as np
import pandas as pd

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask.json import jsonify
from flask_cors import CORS

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt') 

from prometheus_flask_exporter import PrometheusMetrics
##########################################################################
## Application Setup
##########################################################################

app = Flask(__name__)
cors = CORS(app)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Anime Flask App', version='1.0.3')

counter = metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint, 'path': lambda: request.path, 'method':lambda:request.method}
)

##########################################################################
## Load Models
##########################################################################

with open('model/anime_model.pkl', 'rb') as f1:
    # Load the data from the file
    model = pickle.load(f1)

with open('model/vectorizer.pkl', 'rb') as f2:
    # Load the data from the file
    vectorizer = pickle.load(f2)


##########################################################################
## Define Functions
##########################################################################

def remove_digits(string):
    new_string = ""
    for char in string:
        if not char.isnumeric():
            new_string += char
    return new_string


def remove_stop_words(string):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(string)
    filtered_string = [word for word in word_tokens if not word.lower() in stop_words]
    return ' '.join(filtered_string)


def preprocessing(p_df):
  df = p_df.copy(deep=True)

  # Concatenate the features columns
  df['Text'] = df[df.columns[0]] #Title
  for col in [col for col in df.columns if col not in [df.columns[0],'Text', 'Rating']]:
    df["Text"] += " " + df[col]


  df['Text'] = df['Text'].fillna("")
  df['Text'] = df['Text'].apply(lambda x : x.lower() \
                  .replace("[", "") \
                  .replace("]", "") \
                  .replace("'", "") \
                  .replace(",", ""))

  df['Text'] = df['Text'].apply(remove_digits)
  df['Text'] = df['Text'].apply(remove_stop_words)

  X = vectorizer.transform(df['Text'])
  return X
  
  
def predict_rating(df):
  return model.predict(preprocessing(df))[0]


##########################################################################
## Routes
##########################################################################

@app.route("/")
@counter
def home():
    return render_template("home.html")

@app.route("/metrics")
def metrics():
    return metrics.generate_latest()


@app.route('/', methods=['POST'])
def get_anime():

    data = request.json
    return {data}

@app.route('/predict', methods=['POST'])
def predict():
    #request_body = request.form.to_dict()
    request_body = dict(request.json)
    print(request_body)
    query = pd.DataFrame({k:[v] for k,v in request_body.items()})
    print(query)
    return jsonify({'Rating' : predict_rating(query)})

@app.route('/predict_test', methods=['POST'])
def predict_test():
    request_body = request.form.to_dict()
    query = pd.DataFrame({k:[v] for k,v in request_body.items()})
    return jsonify({'Rating' : predict_rating(query)})

##########################################################################
## Main
##########################################################################

if __name__ == '__main__':
    app.run(port=5001)
