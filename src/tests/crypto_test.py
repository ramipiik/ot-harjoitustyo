from sqlite3.dbapi2 import IntegrityError
import unittest
from services.crypto_services import get_crypto_ids
from repositories.crypto_repository import store_cryptos
from repositories.price_repository import store_prices

class TestCrypto(unittest.TestCase):
    def test_get_all_cryptos(self):
        """Checks that all 19 crypto currencies are found from the database"""
        cryptos = get_crypto_ids()
        self.assertEqual(len(cryptos), 19)

    def test_store_cryptos(self):
        """Checks that storing cryptos raises an Integrity error when ran on the existing db"""
        store_cryptos()
        self.assertRaises(IntegrityError)
    
    def test_store_prices(self):
        """Checks that storing prices raises an Integrity error when ran on the existing db"""
        store_prices()
        self.assertRaises(IntegrityError)
