import pandas as pd
import yfinance as yf
import concurrent.futures

data = pd.read_csv('data/nasdaq_screener.csv')

def getPR(symbol):
    sn = None
    pr = None
    try:
        stock = yf.Ticker(symbol)
        pr = stock.info['pegRatio']
        sn = stock.info['shortName']
    except Exception:
        pass
    return (sn, pr)


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(getPR, sym): sym for sym in data['Symbol']}
    for future in concurrent.futures.as_completed(futures):
        sn, pr = future.result()
        if sn:
            print(f'{sn} : {pr}')

print()