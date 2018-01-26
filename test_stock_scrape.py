import unittest
import logging
import sys
import stock_scrape


logging.basicConfig(filename='stock_scrape.log', level=logging.WARNING)

try:
    with open('key.txt', 'r') as f:
        API_KEY = f.readline().strip()
except FileNotFoundError as e:
    print("\n\tA text file containing the API key must be present and in the working directory.\n")
    sys.exit()


class TestStockScrape(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n\tRunning Macro Setup...\n\n')

    @classmethod
    def tearDownClass(cls):
        print('\n\tRunning Macro Tear Down...\n')

    def setUp(self):
        print('\nRunning Micro Setup...\n')

    def tearDown(self):
        print('\nRunning Micro Tear Down...\n\n')

    def test_get_url(self):
        print('Testing get_url(func, sym)...')
        expected = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=KD5IR7D86O9BCZYI"
        result = stock_scrape.get_url("TIME_SERIES_DAILY", "MSFT")
        self.assertEqual(result, expected)

    def test_fswitch(self):
        print('Testing fswitch(x)...')

        expected = "TIME_SERIES_INTRADAY"
        result = stock_scrape.fswitch(1)
        self.assertEqual(result, expected)

        expected = "TIME_SERIES_DAILY"
        result = stock_scrape.fswitch(2)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
