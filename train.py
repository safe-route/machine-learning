# Requirement check
import os
import datetime

# Tensorflow
import tensorflow as tf

# Utils
from utility.constants import *
from utility.utility import *

def create_user_model(username:str):
    """Create user model"""
    if os.path.exists(os.path.join(MODEL_FOLDER, username)):
        # check if model folder for user exist
        return "model for user {} already exist".format(username)
    # create model folder
    if not os.path.exists(MODEL_FOLDER):
        os.mkdir(MODEL_FOLDER)
    # create user's model folder    
    os.mkdir(os.path.join(MODEL_FOLDER, username))
    # create user's model
    try:
        create_model(username)
        return "successfully created model for user {}".format(username)
    except Exception as e:
        return "unable to create model for user {}. {}".format(username, e)


def create_model(username:str):
    """Create Forecasting Model
    Model used: LSTM
    model output consist of 2 item, latitude and longitude
    """
    tf.keras.backend.clear_session()
    # Generating model
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(64, activation='sigmoid', input_shape=(STEPS_SIZE, NUM_OF_FEATURES), return_sequences=True),
        tf.keras.layers.LSTM(32, activation='sigmoid', return_sequences=True),
        tf.keras.layers.LSTM(16, activation='sigmoid'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(16, activation='sigmoid'),
        tf.keras.layers.Dense(8, activation='sigmoid'),
        tf.keras.layers.Dense(NUM_OF_LABELS, activation='linear')
    ])

    # Compiling model
    model.compile(
        loss=LOSS,
        optimizer=OPTIMIZER,
        metrics=METRICS,
    )
    # Save model
    save_model(username, model)

def train_model(username:str, data:dict, **kwargs):
    """Train model with the given tensorflow dataset"""
    # Load model
    model = load_model(username)
    if not model:
        # abort training since model does not exist
        return "model for user {} does not exist".format(username)
    # Train model
    try:
        model.fit(data['train'], epochs=kwargs.get("epochs", EPOCHS),
            validation_data=data['valid'])
    except:
        return "not enough data for training"

    # Test model
    try:
        save_model_evaluation(username,
            model.evaluate(data['test'], return_dict=True))
    except:
        return "not enough data for testing"
    # Save model
    try:
        save_model(username, model)
        return "succesfully trained and saved user {}'s model".format(username)
    except Exception as e:
        return "unable to save user {} model. {}".format(username, e)

def save_model_evaluation(username:str, report:dict):
    """Save model report to user's evaluation log file"""
    if not os.path.exists(os.path.join(MODEL_FOLDER, username)):
        # abort if user's folder does not exist
        return
    with open(os.path.join(MODEL_FOLDER, username, 'evaluate_log.txt'), 'a') as f:
        f.write("{} loss:{} mae:{} mse:{}\n".format(
            datetime.datetime.now().strftime("%Y-%m-%d %T"),
            report.get('loss', 'Unknown'),
            report.get('mae', 'Unknown'),
            report.get('mse', 'Unknown')))