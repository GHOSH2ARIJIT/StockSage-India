from . import views
from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
  
    #path('admin/',admin.site.urls),
    path('', views.finance_topic_detail, name='finance_topic_detail'),
    path('finance-topic-detail/', views.finance_topic_detail, name='finance_topic_detail'),
    path('finance-topic-twocolumn/', views.finance_topic_twocolumn, name='finance_topic_twocolumn'),
    #path('finance-topic-twocolumnset/', views.finance_topic_twocolumnset, name='finance_topic_twocolumnset'),
    path('finance-topic-onecolumn/', views.finance_topic_onecolumn, name='finance_topic_onecolumn'),
    path('end-session/',views.end_session, name='end-session'),
    path('candlestick/', views.candlestick_chart_view, name='candlestick'),
    path('admin/', admin.site.urls),
   # path('', include('stocks.urls')), 
]