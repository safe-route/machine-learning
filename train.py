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
        print("model for user {} already exist".format(username))
        return
    # create user's model folder

    os.mkdir(os.path.join(MODEL_FOLDER, username))
    # create user's model
    create_model(username)

def create_model(username:str):
    """Create Forecasting Model
    Model used: LSTM
    model output consist of 2 item, latitude and longitude
    """
    print('clear session')
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

    print("successfully created model for user {}".format(username))

def train_model(username:str, data:dict, **kwargs):
    """Train model with the given tensorflow dataset"""
    # Load model
    model = load_model(username)
    if not model:
        # abort training since model does not exist
        return
        # Train if model exist
    # Train model
    model.fit(data['train'], epochs=kwargs.get("epochs", EPOCHS),
        validation_data=data['valid'])
    save_model_evaluation(username,
        model.evaluate(data['test'], return_dict=True))
    # Save model
    save_model(username, model)

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