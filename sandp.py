import requests
from bs4 import BeautifulSoup

fname = 'sandp.txt'
url = 'https://en.wikipedia.org/w/api.php'
params = {
    'action': 'parse',
    'prop': 'text',
    'format': 'json',
    'page': 'List_of_S%26P_500_companies',
    'section': 1
}

def gettable():
    resp = requests.get(url, params=params)
    soup = BeautifulSoup(resp.json()['parse']['text']['*'])
    return soup

def gettickers():
    soup = gettable()
    table = soup.find('tbody')
    tickers = []
    for row in table.find_all('tr'):
        ticker = row.find('a').text.strip()
        tickers.append(ticker)
    tickers.pop(0)
    return tickers

def writetickers(tickers):
    with open(fname, 'wt') as fout:
        fout.write('\r\n'.join(tickers))

def main():
    tickers = gettickers()
    writetickers(tickers)


if __name__ == "__min__":
    main()
