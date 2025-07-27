from django.db import models
import yfinance as yf
import pandas as pd
from django.contrib.auth.models import User
import cv2
#print(cv2.__version__)
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
from mongoengine import connect
from pymongo import MongoClient

#Setup MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["stocksage_db"]
footer_collection = db["footer_data"]
webpage_static_collection = db["webpage_static_data"]



# Fetch all users
users = User.objects.all()


def footer_text_data():
    return footer_collection.find_one({}, {'_id': 0})

def web_static_data():
    return webpage_static_collection.find_one({}, {'_id': 0})

def BSE_history_5days(start="2023-01-01",end="2023-12-31"):
    bse_ = yf.Ticker("^BSESN")
    hist = bse_.history(period="5d")
    #df = ticker.history(start , end )
    return pd.DataFrame(hist)

def load_stock_data(input_array):
    # Load the model (this happens once when the module is imported)
    model = tf.keras.models.load_model("lstm_model.h5",compile=False)#path/to/your_model.h5 need to update
    #print(f'model for input shape ******logs: ',model.input_shape)
    # Inference function
    prediction = model.predict(input_array)
    return prediction

class StockPrediction(models.Model):
    # your fields here
    ticker = models.CharField(max_length=10)
    predicted_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.ticker} - {self.predicted_price}"   