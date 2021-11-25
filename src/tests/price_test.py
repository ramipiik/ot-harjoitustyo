import unittest
from services.price_services import get_rates


class TestPrice(unittest.TestCase):
    def test_get_rates(self):
        """Checks that crypto prices are correctly fetched for 2020-01-01"""
        rates:dict = get_rates('2020-01-01')
        self.assertEqual(len(rates.keys()), 19)
        sum=0
        for rate in rates.values():
            sum+=(rate['close'])
        average_price=sum/19
        self.assertAlmostEqual(round(average_price), 401)
        