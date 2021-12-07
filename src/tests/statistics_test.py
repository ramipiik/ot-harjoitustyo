import unittest
from entities.content import Content
from entities.portfolio import Portfolio
from services.user_services import signup
from services.portfolio_services import create_portfolio, INITIAL_CAPITAL, FIRST_DAY
from services.content_services import buy, next_period, get_content
from services.statistic_services import get_price_statistics, get_portfolio_statistics
from entities.user import User
from repositories.user_repository import delete_user
from repositories.portfolio_repository import delete_user_portfolios, read_portfolio_id
from repositories.crypto_repository import read_crypto_ids, CRYPTO_NAMES


class TestContent(unittest.TestCase):
    def setUp(self):
        self.test_user: User = signup("testing", "testing")
        self.test_portfolio: Portfolio = create_portfolio(self.test_user, "test_portfolio", 3)
        self.portfolio_id=read_portfolio_id(self.test_user.username, "test_portfolio")

    def test_price_statistics(self):
        """method for testing price statistics"""
        rates:dict=get_price_statistics(FIRST_DAY)
        self.assertEqual(len(rates.keys()), len(read_crypto_ids()))
        self.assertEqual(rates[1]["name"], CRYPTO_NAMES[0])
        self.assertTrue(rates[1]["sd"]>0)
        self.assertTrue(rates[1]["close"]>0)


    def test_portfolio_statistics(self):
        content_object:Content=get_content(self.test_user, self.portfolio_id)
        self.assertEqual(content_object.portfolio_day, FIRST_DAY)
        investment=1000000
        buy(self.test_portfolio, 1, investment)
        content_object:Content=get_content(self.test_user, self.portfolio_id)
        next_period(content_object)
        stats=get_portfolio_statistics(self.portfolio_id)
        self.assertTrue(stats["sd"]>0)
        self.assertTrue(stats["today"]>0)
        self.assertTrue(stats["all-time"]>0)
        self.assertTrue(stats["d"]>0)
        self.assertTrue(stats["w"]>0)
        self.assertTrue(stats["m"]>0)
        self.assertTrue(stats["y"]=='--')

    def tearDown(self):
        delete_user_portfolios("testing")
        delete_user("testing")