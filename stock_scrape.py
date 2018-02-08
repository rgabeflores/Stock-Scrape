import logging
from urllib.request import urlopen
from urllib.parse import quote
from contextlib import contextmanager
from json import loads, JSONDecodeError
from matplotlib import pyplot
from modules import ux
import sys

'''
    TO-DO
    • Migrate to AlphaVantage API
    • Optimize with generators, decorators, & context managers
    • Implement cleaner exception handling (try,except,else,finally)
    • Use sets to ensure duplicates aren't added

    ex.
        https://alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=KD5IR7D86O9BCZYI
'''

logging.basicConfig(filename='stock_scrape.log', level=logging.INFO)

# Constants
BASE_URL = "https://www.alphavantage.co/query?"

CSV_FILENAME = "portfolio.csv"


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
        return
    else:
        parameters = "function={}&symbol={}&apikey={}".format(func, quote(sym), API_KEY)
        return BASE_URL + parameters


def retrieve(url):
    http_response = urlopen(url).read()
    try:
        json_data = loads(http_response)
    except JSONDecodeError as e:
        print('Data returned did not have valid JSON formatting.')
    else:
        return json_data[list(json_data.keys())[1]]


def parse_json(data):
    for key, value in data.items():
        print('\tDate: {}'.format(key))
        for info_key, info_value in value.items():
            print("\t\t{}: {}".format(info_key, info_value))


# def csv_input(filename=None):
#     if filename is None:
#         filename = input("\n\tEnter the name of the file for input: ")

#     try:
#         with open(filename, "r") as f:
#             file_lines = f.readlines()
#     except FileNotFoundError as e:
#         print("File not found.")
#     else:
#         symbols = (x.strip().split(",") for x in file_lines)
#         for x in symbols:
#             for y in x:
#                 y = y.strip()
#                 with scrape(get_url(fswitch(2), y)) as data:
#                     display(data)
#                     sleep(0.5)

# def update_csv(filename=None):
#     if filename is None:
#         filename = input("\n\tEnter the name of the file for input:\n\t")

#     '''
#     Could be cleaned up with decorators?
#     '''
#     row = input("\n\tEnter stock symbols separated by commas:\n\t")
#     try:
#         with open(filename, "a") as f:
#             print("\tAppending to file...")
#             f.write("\n{}".format(row))
#             print("\tFinished.\n")
#     except FileNotFoundError as e:
#         print("File not found.")
#     try:
#         with open(filename, "r") as f:
#             file_lines = (x for x in f.readlines())
#     except FileNotFoundError as e:
#         print("File not found.")
#     else:
#         print("\tUpdated List:")
#         for line in file_lines:
#             print("\t{}".format(line.strip()))
#         print("\n")


def main():

    def main_loop():
        # choice = ux.get_user_choice(options=MAIN_OPTIONS)

        # if choice == 1:
        #     csv_input(FILENAME)
        # else:
        #     update_csv(FILENAME)

        content = retrieve(get_url(fswitch(2), "MSFT"))
        from pprint import PrettyPrinter
        pp = PrettyPrinter()
        for key in content.keys():
            pp.pprint(content[key])

    ux.to_continue(main_loop)


if __name__ == "__main__":
    main()
