import os
import django

# Replace this path with your actual settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_1.settings')
from django.contrib.auth.models import User

django.setup()

from django.test import TestCase
from django.db import models
import yfinance as yf
import pandas as pd
from django.contrib.auth.models import User
import cv2
print(cv2.__version__)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split 
import ta
from sklearn.preprocessing import MinMaxScaler
# Define LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def load_stock_data_(input_array):
    # Load the model (this happens once when the module is imported)
    model = tf.keras.models.load_model("D:\project\AI_AGENTS\lstm_model.h5")#path/to/your_model.h5 need to update
    print('model loaded')

