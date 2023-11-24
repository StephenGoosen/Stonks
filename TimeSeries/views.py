from django.shortcuts import render
from .models import TimeSeriesData

def time_series_chart(request):
    data = TimeSeriesData.objects.all()
    return render(request, 'timeseries/chart.html', {'data': data})