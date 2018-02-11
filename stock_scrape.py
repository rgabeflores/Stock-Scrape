from urllib.request import urlopen
from urllib.parse import quote
from contextlib import contextmanager
from json import loads, JSONDecodeError
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from datetime import datetime
from modules import ux
import sys
import logging

logging.basicConfig(filename='stock_scrape.log', level=logging.INFO)

BASE_URL = "https://www.alphavantage.co/query?"


def fswitch(x):
    return {
        1: "TIME_SERIES_INTRADAY",
        2: "TIME_SERIES_DAILY"
    }[x]


def get_url(func, sym):
    # LOG FILE IO FOR API KEY
    try:
        with open("../key.txt", 'r') as f:
            API_KEY = f.readline().strip()

    except FileNotFoundError as e:
        print("\n\tA text file containing the API key must be present and in the parent directory.\n")
        logging.critical("key.txt not found.")
        sys.exit()
    else:
        parameters = "function={}&interval=5min&symbol={}&apikey={}".format(func, quote(sym), API_KEY)
        return BASE_URL + parameters


def retrieve(url):
    http_response = urlopen(url).read()
    try:
        json_data = loads(http_response)
    except JSONDecodeError as e:
        print('Data returned did not have valid JSON formatting.')
        sys.exit()
    else:
        return json_data[list(json_data.keys())[1]]


def parse_json(data):
    dates = []
    m_open = []
    m_high = []
    m_low = []
    m_close = []
    m_volume = []
    for date, info in data.items():
        # Intraday API Date Format: %Y-%m-%d %H:%M:%S
        dates.append(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
        m_open.append(float(info['1. open']))
        m_high.append(float(info['2. high']))
        m_low.append(float(info['3. low']))
        m_close.append(float(info['4. close']))
        m_volume.append(float(info['5. volume']))

    return (dates, m_open, m_high, m_low, m_close, m_volume)


def main():
    content = retrieve(get_url(fswitch(1), "MSFT"))
    results = parse_json(content)
    dates = mdates.date2num(results[0])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.setp(ax.get_xticklabels(), rotation=15)

    for i in range(1, len(results) - 1):
        plt.plot_date(dates, results[i], '-')

    plt.xlabel('Dates')
    plt.ylabel('values')
    # plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
