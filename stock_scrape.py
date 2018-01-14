from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from contextlib import contextmanager
from time import sleep

from modules import ux

MAIN_OPTIONS = (
    "View Portfolio",
    "Add Stock Symbol to Portfolio"
)

BASE_URL = "https://finance.yahoo.com/quote/"
FILENAME = "portfolio.csv"


def get_url(param=None):
    if param is None:
        param = quote(input("\n\tSearch for a symbol: ").upper())
    else:
        param = quote(param)
    return "{}?p={}".format(param, param)


@contextmanager
def retrieve(url):
    http_response = urlopen(url).read()
    soup = BeautifulSoup(http_response, 'html.parser')
    content = soup.find('div', {'id': 'quote-summary'})
    yield soup


@contextmanager
def scrape(url, symbol):
    with retrieve(url) as content:
        yield {
            "Stock Symbol": symbol,
            "Previous Close": content.find('td', {'data-test': "PREV_CLOSE-value"}),
            "Open": content.find('td', {'data-test': "OPEN-value"}),
            "Bid": content.find('td', {'data-test': "BID-value"}),
            "Ask": content.find('td', {'data-test': "ASK-value"}),
            "Days Range": content.find('td', {'data-test': "DAYS_RANGE-value"}),
            "52 Week Range": content.find('td', {'data-test': "FIFTY_TWO_WK_RANGE-value"}),
            "Volume": content.find('td', {'data-test': "TD_VOLUME-value"}),
            "Average Volume": content.find('td', {'data-test': "AVERAGE_VOLUME_3MONTH-value"}),
            "Market Cap": content.find('td', {'data-test': "MARKET_CAP-value"}),
            "Beta": content.find('td', {'data-test': "BETA-value"}),
            "PE Ratio (TTM)": content.find('td', {'data-test': "PE_RATIO-value"}),
            "EPS (TTM)": content.find('td', {'data-test': "EPS_RATIO-value"}),
            "Earnings Date": content.find('td', {'data-test': "EARNINGS_DATE-value"}),
            "Forward Dividend & Yield": content.find('td', {'data-test': "DIVIDEND_AND_YIELD-value"}),
            "Ex-Dividend Date": content.find('td', {'data-test': "EXDIVIDEND_DATE-value"}),
            "1Y Target Est": content.find('td', {'data-test': "ONE_YEAR_TARGET_PRICE-value"})
        }


def csv_input(filename=None):
    if filename is None:
        filename = input("\n\tEnter the name of the file for input: ")

    file_lines = []

    try:
        with open(filename, "r") as f:
            file_lines = f.readlines()
    except FileNotFoundError as e:
        print("File not found.")

    symbols = (x.strip().split(",") for x in file_lines)

    for x in symbols:
        for y in x:
            y = y.strip()
            with scrape(BASE_URL + get_url(y), y) as data:
                display(data)
                sleep(0.5)


def update_csv(filename=None):
    if filename is None:
        filename = input("\n\tEnter the name of the file for input:\n\t")

    try:
        with open(filename, "a") as f:
            row = input("\n\tEnter stock symbols separated by commas:\n\t")
            print("\tAppending to file...")
            f.write("\n{}".format(row))
            print("\tFinished.\n")
        with open(filename, "r") as f:
            file_lines = (x for x in f.readlines())
            print("\tUpdated List:")
            for line in file_lines:
                print("\t{}".format(line.strip()))
            print("\n")
    except FileNotFoundError as e:
        print("File not found.")


def display(content):
    ui_separator = "\t\t{}".format("____" * 10)
    print(ui_separator)

    for key in content:
        print("\t\t{}: ".format(str(key)), end="")
        if content[key]:
            if isinstance(content[key], str):
                print(content[key])
            else:
                print(content[key].get_text())
        else:
            print("N/A")
        sleep(0.05)

    print(ui_separator)
    print("\n")


def main():

    def main_loop():
        choice = ux.get_user_choice(options=MAIN_OPTIONS)

        if choice == 1:
            csv_input(FILENAME)
        else:
            update_csv(FILENAME)

    cont = ux.to_continue(main_loop)


if __name__ == "__main__":
    main()
