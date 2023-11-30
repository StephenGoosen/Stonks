import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from django.shortcuts import render
from .forms import StockSelectionForm

def time_series_chart(request):
    data = TimeSeriesData.objects.all()
    return render(request, 'timeseries/chart.html', {'data': data})

def get_stock(request):
    stock_short = yf.Ticker(request)
    hist = stock_short.history(period="1y")

def stock_forecast(request):
    if request.method == 'POST':
        form = StockSelectionForm(request.POST)
        if form.is_valid():
            selected_stock = form.cleaned_data['stock']
            return render(request, 'timeseries/forecast_result.html', {'data': calculated_data})
    else:
        form = StockSelectionForm()

    return render(request, 'timeseries/stock_forecast.html', {'form': form})

def plot_to_base64(fig):
    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    return base64.b64encode(image_stream.getvalue()).decode('utf-8')

def stock_forecast(request):
    if request.method == 'GET':
        form = StockSelectionForm(request.GET)
        if form.is_valid():
            # Process the form data and perform stock forecast
            # Replace the following line with your actual logic
            forecast_data = perform_stock_forecast(form.cleaned_data['stock'])

            # Render a template with the forecast data
            return render(request, 'timeseries/forecast_result.html', {'forecast_data': forecast_data})

    # If the form is not valid or it's not a GET request, render the form
    return render(request, 'timeseries/stock_forecast.html', {'form': form})
