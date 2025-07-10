from ast import Return
from django.shortcuts import render,redirect
from . import models
import yfinance as yf
import pandas as pd
import json, base64,io
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import ta, json


webpage_static_data={'Website_name':'StockSage AI Agent',
                             'heading':'Smarter Investing with AI — Real-Time Indian Stock Market Insights',
                             'live_market':'Analyze, Predict & Optimize your portfolio with cutting-edge AI tailored for NSE & BSE markets.',
                             'predictions':'Using machine learning and time-series models like LSTM and XGBoost, our platform delivers short- and long-term price forecasts with confidence scores.',
                             'visualize':'Access interactive charts with RSI, MACD, Bollinger Bands, and volume overlays — powered by live data from NSE and BSE.',
                             'suggestions':'Get AI-backed stock picks and risk-balanced portfolios based on your goals — whether you\'re a long-term investor or short-term trader.',
                             'sentiment_driven_insight':'We scan news headlines, social media, and regulatory announcements to track real-time sentiment shifts that impact your holdings.',
                             'who_we_are':'StockSage India is a next-gen AI agent built to empower Indian investors with actionable insights. We combine deep learning, natural language processing, and real-time data to simplify market decisions for both new and seasoned traders. Our goal? Smarter investing for everyone.',
                             'Price_Prediction_Models':'Forecast long-term stock trends using LSTM, XGBoost, and more.',
                             'Sentiment_Analysis':'Monitor news and social media to understand market.',
                             'Backtesting_Trading_Strategies':'Simulate and evaluate strategies using historical data.',
                             'Built_for_Indian_Markets':'Specifically tailored for NSE/BSE stocks.',
                             'Secure_and_Private':'Your data is never shared.',
                             'Nifty':'Nifty is Indias benchmark stock market index, representing the top companies listed on the National Stock Exchange (NSE)',                          
                             }
        
website_footer_data={
    'footer1':'Live Stock Prices',													
    'footer2':'Market Overview',
    'footer3':'Top Gainers & Losers',
    'footer4':'Technical Indicators',

    'footer5':'Price Predictions',													
    'footer6':'AI Stock Ratings',
    'footer7':'Intraday Signals',
    'footer8':'Long-Term Forecasts',

    'footer9':'Portfolio Analyzer',													
    'footer10':'Smart Recommendations',
    'footer11':'Compare Stocks',
    'footer12':'Watchlist Manager',

    'footer13':'Market News',
    'footer14':'Sentiment Trends',
    'footer15':'Beginner\'s Guide to Investing',
    'footer16':'How Our AI Works',
    'footer_about_title':'About the Platform',
    'footer_about':'Welcome to StockSage India — your AI-powered stock market companion.We bring together real-time data, cutting-edge machine learning, and financial expertise to simplify investing for everyone. Whether you\'re a beginner looking to understand the Nifty 50 or an experienced trader optimizing your portfolio, our tools help you make smarter, faster decisions in the Indian markets. Explore predictions, track technical indicators, and stay informed with sentiment-driven insights — all from one intelligent dashboard.',
}

def protected_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

def finance_topic_detail(request):  
    if request.user.is_authenticated:
        return render(request, 'webpage_1/index_finance.html',{'page_data':webpage_static_data, 'footer_data':website_footer_data})
    else:
        return redirect('/admin/login/?next=/')


#old function not being used anymore..10-07-2025
def finance_topic_twocolumn(request):
    if request.user.is_authenticated:
       df=models.BSE_history_5days()
       # Convert DataFrame to JSON format
       json_records = df.reset_index().to_json(orient='records')
       data = json.loads(json_records)
       # Pass data to template
       context = {'dataframe': data}
       return render(request, 'webpage_1/twocolumn1.html',context)
    else:
       return redirect('/admin/login/?next=/finance-topic-twocolumn/')
    
    
def finance_topic_twocolumnset(request):
    if request.user.is_authenticated:
      ticker = yf.Ticker("TCS.NS")
      print(ticker,"*******************")
      print("*******************")

      hist = ticker.history(period="6mo")
      print(ticker)
      
      # Select relevant columns
      # Select relevant columns
      data_to_infer = hist[['Close', 'High', 'Low', 'Open', 'Volume']].copy()

      # Add technical indicators
      data_to_infer['RSI'] = ta.momentum.RSIIndicator(data_to_infer['Close'].squeeze()).rsi()
      data_to_infer['MACD'] = ta.trend.MACD(data_to_infer['Close'].squeeze()).macd_diff()
      # Drop rows with NaN values (introduced by technical indicators)
      data_to_infer.dropna(inplace=True)

      # Ensure the order of columns matches the training data
      # Assuming the training data was prepared with 'Close', 'RSI', 'MACD' as features
      # You might need to adjust this based on how your original X_train was structured
      # For this example, let's assume the model expects Close, RSI, MACD.
      # You may need to add other features here if they were used during training.
      data_to_infer = data_to_infer[['Close', 'RSI', 'MACD']]

      # Scale the data using the same scaler fitted on the training data
      # Important: Use the scaler object that was fitted on the training data.
      # If you don't have the scaler from training, you'll need to save and load it.
      # For this example, we'll re-fit a scaler, but in a real scenario, use the saved one.
      # Re-fitting here is for demonstration purposes only and might lead to suboptimal results.
      scaler_infer = MinMaxScaler()
      scaled_data_to_infer = scaler_infer.fit_transform(data_to_infer) # Use the scaler from training!
      # Prepare sequences for inference
      # The sequence length (60 in this case) must match the one used during training
      X_infer = []
      sequence_length = 60 # Must match the training sequence length
      if len(scaled_data_to_infer) >= sequence_length:
          for i in range(sequence_length, len(scaled_data_to_infer) + 1):
             X_infer.append(scaled_data_to_infer[i-sequence_length:i])
      X_infer = np.array(X_infer)

      # Reshape for LSTM input (samples, timesteps, features)
      X_infer = np.reshape(X_infer, (X_infer.shape[0], X_infer.shape[1], X_infer.shape[2]))
      X_infer_reshaped = X_infer[:, :, 0].reshape(X_infer.shape[0], X_infer.shape[1], 1)
      
      #call prediction from model to predict
      predictions_infer_scaled = models.load_stock_data(X_infer_reshaped)
      
      prediction_for_reder = predictions_infer_scaled.flatten().tolist() # 1D array
      print(f'predictions_infer_scaled:::::',predictions_infer_scaled.shape,' prediction_for_reder: for HTML:::::',prediction_for_reder)
      
      
      # inverse the normalization
      
      
      return render(request, 'webpage_1/twocolumn2.html',{'predicted_data':json.dumps(prediction_for_reder),'page_data':webpage_static_data, 'footer_data':website_footer_data})
    else:
       return redirect('/admin/login/?next=/finance-topic-twocolumnset/')
    

def end_session(request):
    request.session.flush()
    return redirect('/admin/logout/') 


