import sys
sys.path.append('/home/steph/ts/Stonks')

import yfinance as yf
import pandas as pd
from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stonks.settings')
application = get_wsgi_application()

from Stonks import settings
from TimeSeries.models import Stock

def fetch_stock_data(symbol):
    stock_data = yf.download(symbol, start='2020-01-01', end='2023-01-01')
    print(f"Data for {symbol}:\n{stock_data}")

stock = yf.Ticker('AAPL')

stock_info = stock.info

print(stock_info)

def download_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def save_stock_data_to_database(stock, data):
    for index, row in data.iterrows():
        stock_data = StockData(
            stock=stock,
            date=index,
            close_price=row['Close']
        )
        stock_data.save()

def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return info
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return {}
    
def main():

    start_date = '2022-01-01'
    end_date = '2023-01-01'

    stock_symbols = ["AAPL", "GOOGL", "MSFT"]

    for symbol in stock_symbols:
        stock_info = get_stock_info(symbol)
        
        # Extract industry information
        industry = stock_info.get('industry', 'Unknown')

        # Get or create the stock with industry information
        stock, created = Stock.objects.get_or_create(
            symbol=symbol,
            defaults={
                'name': stock_info.get('longName', 'N/A'),
                'industry': industry,
            }
        )

        print(f"Stock {stock.symbol} ({stock.name}) - Industry: {industry}")

if __name__ == "__main__":
    main()