# Files
import os

# Tensorflow
import tensorflow as tf

# Dataset
import numpy as np
import pandas as pd
from utility.constants import *

# Measure distance
def distance(coordinate_1:tuple[float,float], coordinate_2:tuple[float, float]) -> float:
    """Measure haversine distance between two coordinate.
    
    Note:
    - coordinate : tuple of latitude and longitude, ex. (3.10326051, 91.23206407)
    Reference: https://en.wikipedia.org/wiki/Haversine_formula
    """
    # constants
    earth_radius = 6371000 # in meters
    
    # unpack and convert params to radian
    lat_1, long_1 = np.radians(coordinate_1)
    lat_2, long_2 = np.radians(coordinate_2)
    
    d_lat = lat_2 - lat_1
    d_long = long_2 - long_1
    
    # calculate and return distance
    return 2 * earth_radius * np.arcsin (np.sqrt(
        np.sin(d_lat/2) ** 2
        + np.cos(lat_1) * np.cos(lat_2) * np.sin(d_long/2) ** 2))
    
distance((-6.200000, 106.816666),(-6.914744, 107.609810))


# Data proceessing
def fetch_dataset(source, type:str="json"):
    """Return a pandas dataframe object from given source"""
    if type.lower()=="json":
        df = pd.DataFrame(source)
        return df
    else:
        return source
    # df = source.to_dataframe()
    # df.rename(columns = {'f0_':'date','lat':'latitude','long':'longitude'}, inplace = True)
    # df["time"] = df["time"].astype("string", errors='ignore')

def preprocess_dataset(data:pd.DataFrame):
    """Preprocess dataset by doing:
    1. convert date to multiple column
    2. convert time to cumulative minute
    3. rearrange fields"""
    # Converting date string to datetime
    data["datetime"] = pd.to_datetime(data["datetime"])
    data["day_of_week"] = data["datetime"].dt.day_of_week
    data["month"] = data["datetime"].dt.month
    data["year"] = data["datetime"].dt.year
    data["time"] = data["datetime"].dt.hour * 60 + data["datetime"].dt.minute

    # Converting time to cumulative minute
    # source: https://stackoverflow.com/questions/17951820/convert-hhmmss-to-minutes-using-python-pandas
    # credit: Andy Hayden
    # data["time"] = data["time"].str.split(':').apply(lambda time: int(time[0]) * 60 + int(time[1]))

    # Removing unused column
    del data["datetime"]

    # Rearrange column
    data = data[["year", "month", "day_of_week", "time", "latitude", "longitude"]]
    return data

def split_dataset(data:pd.DataFrame, train_split:float, test_split:float):
    """Split data to train, valid, and test data"""
    # Split train_valid data and test data
    test_len = test_split
    if type(test_split)==float:
        test_len = int(test_len * len(data))
    train_val_data, test_data = data[:-test_len], data[-test_len:]
    
    # Split train data and valid data
    train_len = int(len(train_val_data) * train_split)
    train_data, valid_data = train_val_data[:train_len], train_val_data[train_len:]
    
    return train_data, valid_data, test_data

def windowed_dataset(data:pd.DataFrame, steps_size:int=STEPS_SIZE,
        predicts_size:int=PREDICTS_SIZE, batch_size:int=BATCH_SIZE,
        shuffle_buffer:int=SHUFFLE_BUFFER_SIZE):
    """Create windowed dataset"""
    # Converting to tfds
    wds = tf.data.Dataset.from_tensor_slices(data)
    
    # Data shifting
    wds = wds.window(steps_size+predicts_size, shift=predicts_size, drop_remainder=True)
    
    # Flatten windows
    wds = wds.flat_map(lambda window : window.batch(steps_size+predicts_size))
    
    # Create window tuples
    wds = wds.map(lambda window: (window[:-predicts_size], window[-predicts_size:, -NUM_OF_LABELS:]))
    
    # Shuffle windows
    wds = wds.shuffle(shuffle_buffer)
    
    # Batch windows
    wds = wds.batch(batch_size).prefetch(1)
    
    return wds

def build_dataset(source, **kwargs):
    """Build dataset to make a train-ready dataset
    list of valid kwargs:
    - test_split: float - split value for test from whole dataset
    - valid_split: float - split value for valid from train_valid dataset
    - steps_size: int - number of steps used for prediction
    - predicts_size: int - number of predictions
    - batch_size: int - dataset batch size
    - shuffle_buffer_size: int - shuffle buffer size
    - num_of_features: int - number of features
    - num_of_labels: int - number of labels
    """
    # BUILD CONSTANTS
    # Data split
    test_split = kwargs.get('test_split', TEST_SPLIT)
    valid_split = kwargs.get('valid_split', VALID_SPLIT)
    train_split = 1 - valid_split

    # Dataset window
    steps_size = kwargs.get('steps_size', STEPS_SIZE)
    predicts_size = kwargs.get('predicts_size', PREDICTS_SIZE)
    window_size = steps_size + predicts_size
    batch_size = kwargs.get('batch_size', BATCH_SIZE)
    shuffle_buffer_size =  kwargs.get('shuffle_buffer_size', SHUFFLE_BUFFER_SIZE)

    # Dataset frame
    num_of_features = kwargs.get('num_of_features', NUM_OF_FEATURES)
    num_of_labels = kwargs.get('num_of_labels',NUM_OF_LABELS)
    
    # FETCHING DATASET
    ds = fetch_dataset(source) # use await for later asynchrounous usage
    
    # PREPROCESSING DATASET
    ds = preprocess_dataset(ds)
    
    # SPLITTING DATASET
    _train_ds, _valid_ds, _test_ds = split_dataset(ds, train_split, test_split)
    
    # WINDOWING AND RETURNING DATASET
    return \
        windowed_dataset(_train_ds, steps_size, predicts_size, batch_size, shuffle_buffer_size), \
        windowed_dataset(_valid_ds, steps_size, predicts_size, batch_size, shuffle_buffer_size), \
        windowed_dataset(_test_ds, steps_size, predicts_size, batch_size, shuffle_buffer_size)

def build_inference_dataset(source, **kwargs):
    """Build inference dataset in the form of prefetch dataset from given source"""
    # BUILD CONSTANTS
    # Data split
    test_split = kwargs.get('test_split', TEST_SPLIT)
    valid_split = kwargs.get('valid_split', VALID_SPLIT)
    train_split = 1 - valid_split

    # Dataset window
    steps_size = kwargs.get('steps_size', STEPS_SIZE)
    predicts_size = kwargs.get('predicts_size', PREDICTS_SIZE)
    window_size = steps_size + predicts_size
    batch_size = kwargs.get('batch_size', BATCH_SIZE)
    shuffle_buffer_size =  kwargs.get('shuffle_buffer_size', SHUFFLE_BUFFER_SIZE)

    # Dataset frame
    num_of_features = kwargs.get('num_of_features', NUM_OF_FEATURES)
    num_of_labels = kwargs.get('num_of_labels',NUM_OF_LABELS)
    
    # FETCHING DATASET
    ds = fetch_dataset(source)
    
    # PREPROCESSING DATASET
    ds = preprocess_dataset(ds)
    
    # CONVERTING TO INFERENCE SHAPE
    if len(ds) != steps_size:
        return None
    ds = ds[-steps_size:] # take only n-steps

    # Add empty row as empty label
    ds.loc[ds.shape[0]] = np.zeros(num_of_features)
    
    # WINDOWING AND RETURNING DATASET
    pfd = windowed_dataset(ds, steps_size, predicts_size, batch_size, shuffle_buffer_size)
    print(pfd)
    return pfd

def calculate_trigger(
        coordinate_1:tuple[float,float],
        coordinate_2:tuple[float,float],
        max_range:float) -> bool:
    """Calculate if distance between two coordinates is 
    over the max range and return True if distance is more
    than max_range"""
    print(distance(coordinate_1, coordinate_2))
    return distance(coordinate_1, coordinate_2) > max_range

def save_model(username:str, model):
    """Save user's model"""
    model.save(os.path.join(MODEL_FOLDER, username, "model.h5"))

def load_model(username:str):
    """Load user's model"""
    if not os.path.exists(os.path.join(MODEL_FOLDER, username, "model.h5")):
        return None
    return tf.keras.models.load_model( \
        os.path.join(MODEL_FOLDER, username, "model.h5"))