import unittest
from entities.content import Content
from entities.portfolio import Portfolio
from services.user_services import signup
from services.portfolio_services import create_portfolio, REFERENCE_STRATEGIES, INITIAL_CAPITAL
from services.content_services import buy, sell, get_content
from entities.user import User
from repositories.user_repository import delete_user
from repositories.portfolio_repository import read_reference_portfolios, delete_user_portfolios, read_portfolio_id


class TestContent(unittest.TestCase):
    def setUp(self):
        self.test_user: User = signup("testing", "testing")
        self.test_portfolio: Portfolio = create_portfolio(self.test_user, "test_portfolio", 1)
        
        
    def test_portfolio_cash(self):
        """method for testing creation of a new portfolio"""
        # print("Hello world")
        # print("********************")

        self.assertEqual(self.test_portfolio.cash, INITIAL_CAPITAL)
        portfolio_id=read_portfolio_id(self.test_user.username, "test_portfolio")

        investment=100000
        buy(self.test_portfolio, 1, investment)
        content_object:Content=get_content(self.test_user, portfolio_id)
        self.assertEqual(content_object.cash, INITIAL_CAPITAL-investment)

        divestment=50000
        sell(self.test_portfolio, 1, divestment)
        content_object:Content=get_content(self.test_user, portfolio_id)
        self.assertEqual(content_object.cash, INITIAL_CAPITAL-investment+divestment)

    def tearDown(self):
        delete_user_portfolios("testing")
        delete_user("testing")