# test_monte_carlo_simulation.py

import unittest
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import the monte_carlo_simulation function from your module
from financial_dashboard import monte_carlo_simulation

class TestMonteCarloSimulation(unittest.TestCase):

    def setUp(self):
        self.start_date = datetime.today() - timedelta(days=365)
        self.end_date = datetime.today()
        dates = pd.date_range(self.start_date, self.end_date)
        self.sample_data = pd.DataFrame({
            'Date': dates,
            'Close': np.random.uniform(100, 200, size=len(dates))
        })
        self.simulations = 100

    def test_monte_carlo_simulation(self):
        results = monte_carlo_simulation(self.sample_data, self.simulations)
        self.assertEqual(len(results), self.simulations)
        self.assertTrue(all(isinstance(value, float) for value in results))

if __name__ == '__main__':
    unittest.main()
