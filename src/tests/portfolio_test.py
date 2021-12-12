import unittest
from entities.portfolio import Portfolio
from services.user_services import signup, login
from services.portfolio_services import create_portfolio, REFERENCE_STRATEGIES, INITIAL_CAPITAL
from entities.user import User
from repositories.user_repository import delete_user
from repositories.portfolio_repository import read_reference_portfolios, delete_user_portfolios, read_portfolio_id


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        if signup("testing", "testing"):
            self.test_user: User = login("testing", "testing")
        self.test_portfolio: Portfolio = create_portfolio(self.test_user, "test_portfolio", 1)
        
        
    def test_portfolio_cash(self):
        """method for testing creation of a new portfolio"""
        self.assertEqual(self.test_portfolio.cash, INITIAL_CAPITAL)
        portfolio_id=read_portfolio_id(self.test_user.username, "test_portfolio")
        reference_portfolios: dict = read_reference_portfolios(portfolio_id)
        for strategy in REFERENCE_STRATEGIES:
            self.assertTrue(strategy in reference_portfolios.keys())

    def tearDown(self):
        delete_user_portfolios("testing")
        delete_user("testing")
        