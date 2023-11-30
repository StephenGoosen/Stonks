from django.urls import path
from .views import time_series_chart, stock_forecast

urlpatterns = [
    path('chart/', time_series_chart, name='time_series_chart'),
    path('stock-forecast/', stock_forecast, name='stock_forecast'),
]