# test_fetch_stock_data.py

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import the fetch_stock_data function from your module
from financial_dashboard import fetch_stock_data

class TestFetchStockData(unittest.TestCase):

    def setUp(self):
        self.symbol = 'AAPL'
        self.start_date = datetime.today() - timedelta(days=365)
        self.end_date = datetime.today()
        dates = pd.date_range(self.start_date, self.end_date)
        self.sample_data = pd.DataFrame({
            'Date': dates,
            'Close': np.random.uniform(100, 200, size=len(dates))
        })

    @patch('your_module_name.yf.Ticker')
    def test_fetch_stock_data_success(self, mock_ticker):
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.return_value = self.sample_data.set_index('Date')

        data = fetch_stock_data(self.symbol, self.start_date, self.end_date)
        self.assertIsNotNone(data)
        self.assertFalse(data.empty)
        self.assertIn('Date', data.columns)
        self.assertIn('Close', data.columns)

    @patch('your_module_name.yf.Ticker')
    def test_fetch_stock_data_failure(self, mock_ticker):
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.history.side_effect = Exception("Data fetch error")

        data = fetch_stock_data('INVALID', self.start_date, self.end_date)
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
