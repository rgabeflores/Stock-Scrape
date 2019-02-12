from urllib.request import urlopen
from urllib.parse import quote
from contextlib import contextmanager
from json import loads, JSONDecodeError
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from datetime import datetime
import numpy as np
import pandas as pd
import sys
import logging

# By default, info is logged to stock_scrape.log
logging.basicConfig(filename='stock_scrape.log', level=logging.INFO)

BASE_URL = "https://www.alphavantage.co/query?"


def fswitch(x):
    '''
        Acts as a switch case
    '''
    return {
        1: "TIME_SERIES_INTRADAY",
        2: "TIME_SERIES_DAILY"
    }[x]


def get_url(func, sym):
    '''
        Generates the API call based on user input and a key file containing the unique API key
    '''
    try:
        with open("../key.txt", 'r') as f:
            API_KEY = f.readline().strip()

    except FileNotFoundError as e:
        print("\n\tA text file containing the API key must be present and in the parent directory.\n")
        logging.critical("key.txt not found.")
        sys.exit()
    else:
        # interval parameter Hard Coded for TIME_SERIES_INTRADAY API
        parameters = "function={}&symbol={}&apikey={}".format(func, quote(sym), API_KEY)
        return BASE_URL + parameters


def retrieve(url):
    '''
        Makes a request to the AlphaVantage API
    '''
    http_response = urlopen(url).read()
    try:
        json_data = loads(http_response)
    except JSONDecodeError as e:
        print('Data returned did not have valid JSON formatting.')
        sys.exit()
    except Exception as e:
        print(e)
    else:
        return json_data[list(json_data.keys())[1]]


def build_frame(data):
    '''
        Returns a pandas.DataFrame object with OPEN,HIGH,LOW,CLOSE,VOLUME columns/attributes.
    '''
    dates = []
    rows = []

    for date, info in data.items():
        # Intraday API Date Format: %Y-%m-%d %H:%M:%S
        dates.append(datetime.strptime(date, '%Y-%m-%d'))
        rows.append(np.array([
            float(info['1. open']),
            float(info['2. high']),
            float(info['3. low']),
            float(info['4. close']),
            # float(info['5. volume'])
        ]))
    return pd.DataFrame(rows, index=dates, columns=['OPEN', 'HIGH', 'LOW', 'CLOSE'])


def main():
    symbol = 'MSFT' # MSFT (Microsoft) is hardcoded as an example
    content = retrieve(get_url(fswitch(2), symbol))
    df = build_frame(content)

    # X-Axis Date Display Configurations
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # plt.setp(ax.get_xticklabels(), rotation=15)

    # for i in range(1, len(results) - 1):
    #     plt.plot_date(dates, results[i], '-')
    # print(df.describe())
    # plt.plot(df)

    for key in df:
        plt.plot(df[key], label=key)
    plt.title(symbol)
    plt.xlabel('Dates')
    plt.ylabel('Values')
    plt.grid(True, color='k', linestyle='-')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
