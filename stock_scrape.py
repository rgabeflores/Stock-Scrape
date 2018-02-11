from urllib.request import urlopen
from urllib.parse import quote
from contextlib import contextmanager
from json import loads, JSONDecodeError
from matplotlib import pyplot
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
        parameters = "function={}&symbol={}&apikey={}".format(func, quote(sym), API_KEY)
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


def parse_values(data):
    for key, value in data.items():
        print('\tDate: {}'.format(key))
        for info_key, info_value in value.items():
            print("\t\t{}: {}".format(info_key, info_value))


def main():
    content = retrieve(get_url(fswitch(2), "MSFT"))
    parse_json(content)


if __name__ == "__main__":
    main()
