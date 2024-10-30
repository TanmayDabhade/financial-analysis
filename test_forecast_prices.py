# test_forecast_prices.py

import unittest
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import the forecast_prices function from your module
from financial_dashboard import forecast_prices

class TestForecastPrices(unittest.TestCase):

    def setUp(self):
        self.start_date = datetime.today() - timedelta(days=365)
        self.end_date = datetime.today()
        dates = pd.date_range(self.start_date, self.end_date)
        self.sample_data = pd.DataFrame({
            'Date': dates,
            'Close': np.random.uniform(100, 200, size=len(dates))
        })

    def test_forecast_prices(self):
        forecast = forecast_prices(self.sample_data)
        self.assertIsNotNone(forecast)
        self.assertIn('ds', forecast.columns)
        self.assertIn('yhat', forecast.columns)
        self.assertIn('yhat_lower', forecast.columns)
        self.assertIn('yhat_upper', forecast.columns)

if __name__ == '__main__':
    unittest.main()
