import unittest
from services.user_services import signup
from services.portfolio_services import create_portfolio
from entities.user import User
from entities.content import Content
from repositories.user_repository import delete_user


class TestPortfolio(unittest.TestCase):
    def test_portfolio(self):
        """method for testing creation of a new portfolio"""
        test_user: User = signup("testing", "testing")
        test_portfolio: Content = create_portfolio(test_user, "test_porfolio", 1)
        delete_user("testing")
        self.assertEqual(test_portfolio.cash, 1000000)
