import unittest
from services.crypto_services import get_crypto_ids

class TestCrypto(unittest.TestCase):
    def test_get_all_cryptos(self):
        """Checks that all 19 crypto currencies are found from the database"""
        cryptos=get_crypto_ids()
        self.assertEqual(len(cryptos),19)