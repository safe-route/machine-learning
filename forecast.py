# Tensorflow
import tensorflow as tf

# Utils
from utility.constants import *
from utility.utility import *
from utility.mail_sender import *

# Prediction function
def predict_model(username:str, data, email:str, user_location:tuple):
    """Predict and send email if it triggers ccalculate_trigger function"""
    # Check if data is not none
    if data is None:
        return "not enough data for prediction"
    # Load model
    model = load_model(username)
    if not model:
        # abort training since model does not exist
        return "model for user {} does not exist".format(username)
    # Do prediction
    prediction = model.predict(data)[0]
    
    # Fire send_email endpoint
    if calculate_trigger(prediction, user_location):
        # Fire cloud function endpoint
        create_send_email(email, username)
        return "abnormal movement detected for user {}".format(username)
    return "no abnormal movement detected for user {}".format(username)


# Trigger function
def calculate_trigger(
        coordinate_1:tuple[float,float],
        coordinate_2:tuple[float,float],
        max_range:float=MAX_RANGE) -> bool:
    """Calculate if distance between two coordinates is 
    over the max range and return True if distance is more
    than max_range"""
    return distance(coordinate_1, coordinate_2) > max_range