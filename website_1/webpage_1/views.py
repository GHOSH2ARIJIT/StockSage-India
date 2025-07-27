from ast import Return
from django.shortcuts import render,redirect
from . import models
import pandas as pd
import json, base64,io
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import ta, json
from .models import StockPrediction
from datetime import date
import requests
from pymongo import MongoClient
import plotly.graph_objs as go



def get_indicator_data(instrument_key, interval, to_date, from_date):
    access_token = 'r*eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI0M0NXSFAiLCJqdGkiOiI2ODgyNGQ0MTkzOGI4MzY2MDYzYzEzNjIiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6ZmFsc2UsImlhdCI6MTc1MzM2OTkyMSwiaXNzIjoidWRhcGktZ2F0ZXdheS1zZXJ2aWNlIiwiZXhwIjoxNzUzMzk0NDAwfQ.BCSAxuyHxsw5FljUgaUpYtxEfGmjphXyjj63oAM-11E'  # Your actual token

    if not interval:
        interval = "day"
    if not to_date:
        to_date = "2025-03-19"
    if not from_date:
        from_date = "2023-11-12"

    url = f"https://api.upstox.com/v2/historical-candle/{instrument_key}/{interval}/{to_date}/{from_date}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def plot_candlestick_chart(candlestick_data):
    if (
        candlestick_data
        and candlestick_data['status'] == 'success'
        and candlestick_data['data']
        and candlestick_data['data']['candles']
    ):
        candles = candlestick_data['data']['candles']
        df = pd.DataFrame(candles, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Other'])
        df['Date'] = pd.to_datetime(df['Date'])
        fig = go.Figure(data=[
            go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )
        ])
        fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
        # Return HTML to embed in Django template:
        return fig.to_html(full_html=True)
    else:
        return "<p>Could not retrieve candlestick data from the API response.</p>"

def candlestick_chart_view(request):
    if request.user.is_authenticated:
        footer_mongodata=models.footer_text_data()
        webpage_static_data=models.web_static_data()
        # You can pass parameters dynamically (GET/POST) or hardcode for demo
        data = get_indicator_data("NSE_EQ|INE002A01018", "day", "2025-03-19", "2020-11-12")
    
        chart_html = plot_candlestick_chart(data)
        #print(f'calling finance_topic_twocolumnset',chart_html)
        return render(request, 'webpage_1/candlestick_chart.html', {'page_data':webpage_static_data, 'footer_mongodata':footer_mongodata,'chart_html': chart_html})
    else:
       return redirect('/admin/login/?next=/candlestick/')


def save_to_mongo_from_django(request):
    data = {
        "company": "TCS",
        "prediction": "Buy"
    }
    response = requests.post("http://127.0.0.1:8000/fastapi/save/", json=data)
    return JsonResponse({"mongo_response": response.json()})

def show_predictions(request):
    predictions = StockPrediction.objects.filter(company="TCS").order_by('-prediction_date')
    return render(request, 'your_template.html', {'predictions': predictions})


def protected_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

def finance_topic_detail(request):  
    if request.user.is_authenticated:
        footer_mongodata=models.footer_text_data()
        webpage_static_data=models.web_static_data()
        return render(request, 'webpage_1/index_finance.html',{'page_data':webpage_static_data, 'footer_mongodata':footer_mongodata})
    else:
        return redirect('/admin/login/?next=/')


def finance_topic_onecolumn(request):  
    if request.user.is_authenticated:
     footer_mongodata=models.footer_text_data()
     webpage_static_data=models.web_static_data()
     return render(request, 'webpage_1\onecolumn.html',{'page_data':webpage_static_data,  'footer_mongodata':footer_mongodata})
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
    
    

    if request.user.is_authenticated: 
      # inverse the normalization
      
      footer_mongodata=models.footer_text_data()
      webpage_static_data=models.web_static_data()
      #print(f'this has footer data************************',footer_mongodata)
      return render(request, 'webpage_1/twocolumn2.html',{'page_data':webpage_static_data,  'footer_mongodata':footer_mongodata})
    else:
      return redirect('/admin/login/?next=/finance-topic-twocolumnset/')
    

def end_session(request):
    request.session.flush()
    return redirect('/admin/logout/') 


