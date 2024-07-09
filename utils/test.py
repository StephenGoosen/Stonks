import yfinance as yf
import pandas as pd

stock = yf.Ticker('AAPL')

stock_info = stock.history(period="100y")

long_name = stock.info["industry"]

print(stock.info['exchange'])

print(stock.info['phone'])
print(stock.info['longBusinessSummary'])

print(long_name)