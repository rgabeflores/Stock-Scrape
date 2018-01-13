from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
from time import sleep

import ux
import statistics as stats

'''
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
	"Enter a Symbol for a Quote",
	"Get Quotes via CSV File Input"
)

BASE_URL = "https://finance.yahoo.com/quote/"

def get_url(param=None):
	if param is None:
		param = quote(input("\n\tSearch for a symbol: ").upper())
	else:
		param = quote(param)
	return param + "?p=" + param

def retrieve(url):

	http_response = urlopen(url).read()
	soup = BeautifulSoup(http_response, 'html.parser')

	content = soup.find('div', {'id': 'quote-summary'})
	
	#	First Column -------------------------
	p_close = content.find('td', {'data-test': "PREV_CLOSE-value"})
	open_value = content.find('td', {'data-test': "OPEN-value"})
	bid = content.find('td', {'data-test': "BID-value"})
	ask = content.find('td', {'data-test': "ASK-value"})
	days_range = content.find('td', {'data-test': "DAYS_RANGE-value"})
	ftw_range = content.find('td', {'data-test': "FIFTY_TWO_WK_RANGE-value"})
	volume = content.find('td', {'data-test': "TD_VOLUME-value"})
	avg_volume = content.find('td', {'data-test': "AVERAGE_VOLUME_3MONTH-value"})
	#	Second Column ------------------------
	m_cap = content.find('td', {'data-test': "MARKET_CAP-value"})
	beta = content.find('td', {'data-test': "BETA-value"})
	pe_ratio = content.find('td', {'data-test': "PE_RATIO-value"})
	eps = content.find('td', {'data-test': "EPS_RATIO-value"})
	earn_date = content.find('td', {'data-test': "EARNINGS_DATE-value"})
	f_div_yield = content.find('td', {'data-test': "DIVIDEND_AND_YIELD-value"})
	ex_div = content.find('td', {'data-test': "EXDIVIDEND_DATE-value"})
	y_targ_est = content.find('td', {'data-test': "ONE_YEAR_TARGET_PRICE-value"})

	return {
		"Previous Close": p_close,
		"Open": open_value,
		"Bid": bid,
		"Days Range": days_range,
		"52 Week Range": ftw_range,
		"Volume": volume,
		"Average Volume": avg_volume,
		"Market Cap": m_cap,
		"Beta": beta,
		"PE Ratio (TTM)": pe_ratio,
		"EPS (TTM)": eps,
		"Earnings Date": earn_date,
		"Forward Dividend & Yield": f_div_yield,
		"Ex-Dividend Date": ex_div,
		"1Y Target Est": y_targ_est
	}

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

def cli_input():
	url = BASE_URL + get_url()

	rows = retrieve(url)

	display(rows)

def csv_input(filename=None):
	if filename is None:
		filename = input("Enter the name of the file for input: ")
	try:
		with open(file, "r") as f_obj:
			file_lines = f_obj.readlines()
	except IOError as e:
		print("File not found.")
	

				

def main():

	cont = True
	input_filename = "input.txt"

	while cont:
		choice = ux.get_user_choice(options=MAIN_OPTIONS)

		if choice == 1:
			cli_input()
		else:
			csv_input(input_filename)
		

		cont = ux.to_continue()
	

if __name__ == "__main__":
	main()