import os

# Local
from utility.utility import *
from utility.constants import *
from train import *
from forecast import *

# Flask
from flask import Flask, request

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 8080))
HOST = '0.0.0.0'

@app.route("/create", methods=["GET"])
def create():
    username = request.args.get('username', default = 'None', type = str)
    # Get data
    return create_user_model(username)

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
    if not os.path.exists(MODEL_FOLDER):
        # create model folder
        os.mkdir(MODEL_FOLDER)
    if not os.path.exists(DATASET_FOLDER):
        # create dataset folder
        os.mkdir(DATASET_FOLDER)
    app.run(port=PORT, host=HOST, debug=True)