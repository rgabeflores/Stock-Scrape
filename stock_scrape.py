from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from contextlib import contextmanager
import re
from time import sleep
import psutil
import os

import ux
import statistics as stats

def memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

'''
	Quickly track a portfolio.

	List Pages ex.
	https://finance.yahoo.com/world-indices

	Individual Summary Page Quote ex.
	https://finance.yahoo.com/quote/%5EGSPC?p=%5EGSPC (S&P 500)

	• Search Options?
		- Search by comma separated input list?
	• File I/O (txt, csv, spreadsheet, etc.)
		- Quick Balance Sheet Analysis
		- Use a text file to quickly feed search args
		- Use text file to save popular stock symbols
		- Feed Menu Options from text file args?
	• Implement  visuals
		- Graphs
		- Momentum Screening
'''

MAIN_OPTIONS = (
	"View Portfolio",
	"Add Stock Symbol to Portfolio"
)

BASE_URL = "https://finance.yahoo.com/quote/"

def get_url(param=None):
	if param is None:
		param = quote(input("\n\tSearch for a symbol: ").upper())
	else:
		param = quote(param)
	return param + "?p=" + param

@contextmanager
def retrieve(url):
	http_response = urlopen(url).read()
	soup = BeautifulSoup(http_response, 'html.parser')
	content = soup.find('div', {'id': 'quote-summary'})
	yield soup

@contextmanager
def scrape(url):
	'''
		TO-DO:
		• Scrape Labels to get keys
		• Use Generator
	'''
	with retrieve(url) as content: 
		yield {
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
			with scrape(BASE_URL + get_url(y.strip())) as data:
				display(data)
				sleep(1)

def display(content):
	print("\n\n\t\t" + ("____" * 10))
	print("\t\t" + ("____" * 10))

	for key in content:
		print("\t\t" + ("----" * 10))
		print("\t\t" + str(key) + ": ", end="")
		if not(content[key] is None):
			print(content[key].get_text())
		else:
			print("N/A")
		print("\t\t" + ("----" * 10))
		sleep(0.05)

	print("\t\t" + ("____" * 10))
	print("\t\t" + ("____" * 10) + "\n\n")				

def main():

	def main_loop():
		choice = ux.get_user_choice(options=MAIN_OPTIONS)

		if choice == 1:
			csv_input()
		else:
			csv_input()
		
	cont = ux.to_continue(main_loop)

if __name__ == "__main__":
	main()