from repositories.price_repository import store_prices
from repositories.crypto_repository import store_cryptos
from services.crypto_services import get_crypto_ids
from sqlite3.dbapi2 import IntegrityError
import unittest
from initiate_db import initialize_database
initialize_database()


class TestCrypto(unittest.TestCase):
    def setUp(self):
        initialize_database()

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
