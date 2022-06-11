# Files
import os

# Tensorflow
import tensorflow as tf

# Model
LEARNING_RATE = 5e-2
OPTIMIZER = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
LOSS = tf.keras.losses.Huber()
METRICS = ["mae", "mse"]
EPOCHS = 1000

# Data split
TEST_SPLIT = 0.1                # Float or int
VALID_SPLIT = 0.1               # Float
TRAIN_SPLIT = 1 - VALID_SPLIT   # Float

# Dataset window
STEPS_SIZE = 15               # minutes
PREDICTS_SIZE = 1             # minute(s)
WINDOW_SIZE = STEPS_SIZE + PREDICTS_SIZE
BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 64

# Dataset frame
NUM_OF_FEATURES = 6
NUM_OF_LABELS = 2

# Folder
MODEL_FOLDER = os.path.join('.','model')
DATASET_FOLDER = os.path.join('.','dataset')

# Misc
MAX_RANGE = 2000 # max prediction distance range (in km)

# File
DATASET_FILE_1 = './dataset/user_1/usr_1_w1_y2022.csv'
DATASET_FILE_2 = './dataset/user_1/usr_1_w2_y2022.csv'
MODEL_1_FILE = './model/user_1/'
