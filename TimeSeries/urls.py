from django.urls import path
from .views import time_series_chart

urlpatterns = [
    path('chart/', time_series_chart, name='time_series_chart'),
]