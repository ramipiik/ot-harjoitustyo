import math
from repositories.price_repository import read_prices
from services.crypto_services import get_crypto_ids


CRYPTO_IDS=get_crypto_ids()

class Content:
    """Class for managing portfolio content"""

    def __init__(self, portfolio_id, portfolio_day, cash, change_id):
        self.portfolio_id = portfolio_id
        self.portfolio_day = portfolio_day
        self.cash = cash
        self.change_id = change_id
        self.cryptos = {}

    def buy(self, crypto_id, investment):
        """Method for buying a crypto"""
        if crypto_id not in CRYPTO_IDS:
            return ((False, "There is no such crypto"))
        if math.floor(investment) > self.cash:
            return ((False, f"You only have {self.cash} EUR cash."))
        self.cash -= investment
        date = self.portfolio_day
        self.change_id += 1
        prices = read_prices(date)
        price = prices[crypto_id]["close"]
        if crypto_id in self.cryptos:
            before = self.cryptos[crypto_id]["amount"]
            after = before + investment / price
            self.cryptos[crypto_id]["amount"] = after
            self.cryptos[crypto_id]["value"] = after * price
        else:
            self.cryptos[crypto_id] = {}
            self.cryptos[crypto_id]["amount"] = investment / price
            self.cryptos[crypto_id]["value"] = investment
        return True

    def _sell(self, crypto_id, investment):
        """Method for buying a crypto. Allows short selling."""
        if crypto_id not in CRYPTO_IDS:
            return ((False, "There is no such crypto"))
        self.cash += investment
        date = self.portfolio_day
        self.change_id += 1
        prices = read_prices(date)
        price = prices[crypto_id]["close"]
        if crypto_id in self.cryptos:
            before = self.cryptos[crypto_id]["amount"]
            after = before - investment / price
            self.cryptos[crypto_id]["amount"] = after
            self.cryptos[crypto_id]["value"] = after * price
        else:
            self.cryptos[crypto_id] = {}
            self.cryptos[crypto_id]["amount"] = -investment / price
            self.cryptos[crypto_id]["value"] = -investment
        return True
