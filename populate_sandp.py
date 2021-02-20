import yfinance as yf
from time import sleep
from random import random
from sandp import gettickers
from models import get_session, Series

features = ['Open', 'Close', 'High', 'Low', 'Volume']

def process_history(s, ticker, history):
    first = history.index[0].to_pydatetime().date()
    last = history.index[-1].to_pydatetime().date()
    for feature in features:
        json = history[feature].to_json()
        series = Series()
        series.kind = f"stock:{feature}:{ticker.ticker}"
        series.first = first
        series.last = last
        series.series = json
        s.add(series)


def main():
    tickers = gettickers()
    s = get_session()
    series = s.query(Series).all()
    goods = set()
    for serie in series:
        goods.add(serie.kind.split(':')[-1])
    for ticker in goods:
        pos = tickers.index(ticker)
        tickers.pop(pos)
    for ticker in tickers:
        ticker = ticker.replace('.', '-')
        try:
            ticker = yf.Ticker(ticker)
            hist = ticker.history(period="1y")
            process_history(s, ticker, hist)
        except:
            sleep(random()*10+20)
            continue
        print("Processed", ticker.ticker)
        s.commit()
        sleep(random()*10+20)

if __name__ == "__main__":
    main()
