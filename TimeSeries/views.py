import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from django.db import connection
from django.shortcuts import render, HttpResponse
from .forms import StockSelectionForm
from Stonks.settings import BASE_DIR

def stocks_page(request):
    if request.method == 'POST':
        # Get selected stock and number of years from the form
        stock_symbol = request.POST.get('stock_symbol')
        num_years = int(request.POST.get('num_years'))

        # Retrieve stock data using yfinance
        stock_data = yf.download(stock_symbol, period=f'{num_years}y')

        # Call plot1 function to generate the plot and get the image URL
        image_url = plot1(stock_data['Close'], stock_symbol, num_years)

        return render(request, 'stocks_page.html', {
            'image_url': image_url, 
            'name': stock_symbol, 
            'stock_symbols': get_stock_symbols()
        })

    return render(request, 'stocks_page.html', {
        'image_url': None, 
        'stock_symbols': get_stock_symbols()
    })

def get_stock_symbols():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT symbol FROM TimeSeries_stock")
        stock_symbols = [row[0] for row in cursor.fetchall()]
    return stock_symbols

def plot1(data, name, time):
    plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.title(f'{name} Closing Prices Over {time} Years', fontsize=20)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the BytesIO object to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Generate the image URL for the HTML template
    image_url = f'data:image/png;base64,{image_base64}'
    return image_url

def test_image(request):
    # Sample data for testing
    data = yf.download('A', period=f'3y') 
    name = "Sample Stock"  

    plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.title(f'{name} Closing Prices Over Time', fontsize=20)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


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
