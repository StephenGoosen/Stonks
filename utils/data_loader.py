'''
The following code locates the symbols in the yfinance database, and
extracts descriptive information to be stored in the Stock table. The
symbols used for extraction are taken from the nasdaq screener:
https://www.nasdaq.com/market-activity/stocks/screener. 
'''

import sys
sys.path.append('/home/steph/ts/Stonks')

import os
import sqlite3
import pandas as pd
import yfinance as yf
import concurrent.futures
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Locate Database settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stonks.settings')
application = get_wsgi_application()

from TimeSeries.models import Stock
              
attributes_to_extract = ["symbol", "currency", "longName", "sector", "industry", "exchange", "phone", "longBusinessSummary"]

with sqlite3.connect('db.sqlite3') as conn:
    # Function to create a table in the database
    def create_table():
        cursor = conn.cursor()
        Stock.objects.all().delete()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_attributes (
                stock_short TEXT PRIMARY KEY,
                symbol TEXT,
                currency TEXT,
                longName TEXT,
                sector TEXT,
                industry TEXT,
                exchange TEXT,
                phone TEXT,
                longBusinessSummary TEXT
            )
        ''')
        conn.commit()

    # Function to insert data into the database
    def insert_data(data_list):
        Stock.objects.bulk_create([
            Stock(
                symbol=data['symbol'],
                currency=data['currency'],
                sector=data['sector'],
                longName=data['longName'],
                industry=data['industry'],
                exchange=data['exchange'],
                phone=data['phone'],
                longBusinessSummary=data['longBusinessSummary']
            )
            for data in data_list
        ])

    # extractAttributes function
    def extractAttributes(stockShort):
        try:
            x = yf.Ticker(stockShort)
            tickers_data = {}
            temp = pd.DataFrame.from_dict(x.info, orient="index")
            temp.reset_index(inplace=True)
            temp.columns = ["Attribute", "Recent"]
            tickers_data[stockShort] = temp

            # Empty dictionary for Results
            result_dict = {}

            # Loop through each attribute and extract the corresponding "Recent" value
            for attribute in attributes_to_extract:
                try:
                    # Extract the "Recent" value for the current attribute
                    recent_value = tickers_data[stockShort].loc[
                        tickers_data[stockShort]["Attribute"] == attribute, "Recent"
                    ].values[0]

                    # Add the result to the dictionary
                    result_dict[attribute] = recent_value

                except IndexError:
                    # Indicate when attribute is not found and return NA value
                    print(f"Attribute not found for {stockShort}: {attribute}")
                    result_dict[attribute] = None 

            return result_dict
        
        except Exception as e:
            logger.error(f"Error for {stockShort}: {e}")
            return None
    
    # extractAttributesLoop function loops through each symbol
    def extractAttributesLoop(stock_list):

        create_table()

        # List to store data for bulk insertion
        data_list = []

        # Loop through a list of short name stocks
        for stock_short in stock_list:

            # Call the extractAttributes function for each stock
            result_dict = extractAttributes(stock_short)
            data_list.append(result_dict)

        # Insert data into the database in bulk
        insert_data(data_list)

    # Read stock short names from CSV file
    data = pd.read_csv('utils/stock_mega-to-medium.csv')
    stock_list_from_csv = data['Symbol'].tolist()

    # Import Data from yfinance into database
    extractAttributesLoop(stock_list_from_csv)