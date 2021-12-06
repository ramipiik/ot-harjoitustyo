import math
from repositories.price_repository import read_prices
from services.crypto_services import get_crypto_ids
from ui.styles import bcolors, ERROR_MESSAGE


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
        if math.floor(investment) > self.cash:
            print(f"{bcolors.FAIL}--------------------")
            print("Not enough cash")
            print("self.cash", self.cash)
            print(f"--------------------{bcolors.ENDC}")
            return False
        crypto_ids = get_crypto_ids()
        if crypto_id not in crypto_ids:
            print(ERROR_MESSAGE)
            return False
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
            print("moi")
        else:
            self.cryptos[crypto_id] = {}
            self.cryptos[crypto_id]["amount"] = investment / price
            self.cryptos[crypto_id]["value"] = investment
            print(self.cryptos)
        return True

    def sell(self, crypto_id, investment):
        """Method for buying a crypto. Allows short selling."""
        crypto_ids = get_crypto_ids()
        if crypto_id not in crypto_ids:
            print(ERROR_MESSAGE)
            return False
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
