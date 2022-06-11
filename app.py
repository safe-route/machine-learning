import os
import pandas as pd

# Local
from utility.utility import *
from utility.constants import *
from train import *
from forecast import *

# Flask
from flask import Flask, request

app = Flask(__name__)

@app.route("/create", methods=["GET"])
def create():
    username = request.args.get('username', default = 'None', type = str)
    # Get data
    create_user_model(username)
    return "User model created"

@app.route("/train", methods=["POST"])
def train():
    username = request.args.get('username', default = 'None', type = str)
    # Get data
    jobject = request.json
    train, valid, test = build_dataset(jobject["data"])
    data = {
        'train':train,
        'valid':valid,
        'test':test
    }
    train_model(username, data)
    return "Train Finished"

@app.route("/forecast", methods=["POST"])
def forecast():
    username = request.args.get('username', default = 'None', type = str)
    guardian_email = request.args.get('guardian_email', default = 'None', type = str)
    # Get data
    jobject = request.json
    guardian_email = jobject["email"]
    location = (jobject["latitude"], jobject["longitude"])
    data = build_inference_dataset(jobject["data"])
    predict_model(username, data, guardian_email, location)
    return "Forecast finished"
    
if __name__ == "__main__":
    app.run(debug=True)