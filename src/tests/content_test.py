import unittest
from entities.content import Content
from entities.portfolio import Portfolio
from services.user_services import login, signup
from services.portfolio_services import create_portfolio, INITIAL_CAPITAL, FIRST_DAY
from services.content_services import (
    buy,
    coordinate_reference_actions,
    next_period,
    sell,
    get_content,
)
from entities.user import User
from repositories.user_repository import delete_user
from repositories.portfolio_repository import delete_user_portfolios, read_portfolio_id
from repositories.content_repository import read_portfolio_content


class TestContent(unittest.TestCase):
    def setUp(self):
        if signup("testing", "testing"):
            self.test_user: User = login("testing", "testing")
        self.test_portfolio: Portfolio = create_portfolio(
            self.test_user, "test_portfolio", 1
        )
        self.portfolio_id = read_portfolio_id(self.test_user.username, "test_portfolio")

    def test_initial_cash(self):
        """method for testing portfolio creation and initial capital"""
        self.assertEqual(self.test_portfolio.cash, INITIAL_CAPITAL)

    def test_buying_and_selling(self):
        """method for testing buying and selling"""

        investment = 100000
        buy(self.test_portfolio, 1, investment)
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        self.assertEqual(content_object.cash, INITIAL_CAPITAL - investment)

        divestment = 50000
        sell(self.test_portfolio, 1, divestment)
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        self.assertEqual(content_object.cash, INITIAL_CAPITAL - investment + divestment)

    def test_buying_without_money(self):
        """method for testing to invest more than there is money"""
        investment = 1000001
        buy(self.test_portfolio, 1, investment)
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        self.assertEqual(content_object.cash, INITIAL_CAPITAL)

    def test_buying_nonexisting_crypto(self):
        """method for testing to invest more than there is money"""
        investment = 100
        buy(self.test_portfolio, 30, investment)
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        self.assertEqual(content_object.cash, INITIAL_CAPITAL)

    def test_short_selling(self):
        """method for testing to short sell a stock"""
        divestment = 1000000
        sell(self.test_portfolio, 19, divestment)
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        self.assertEqual(content_object.cash, INITIAL_CAPITAL + divestment)

    def test_portfolio_content(self):
        """method for testing that portfolio content is updated after transactions"""
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        self.assertEqual(len(content_object.cryptos.keys()), 0)
        buy(self.test_portfolio, 1, 100)
        buy(self.test_portfolio, 2, 200)
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        content = get_content(self.test_user, self.portfolio_id)[2]
        self.assertFalse(3 in content_object.cryptos.keys())
        self.assertTrue(1 == content[0][2])
        self.assertTrue(2 == content[1][2])

    def test_next_period(self):
        """method for checking that date is updated when moving to next period"""
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        self.assertEqual(content_object.portfolio_day, FIRST_DAY)
        next_period(content_object)
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        self.assertNotEqual(content_object.portfolio_day, FIRST_DAY)

    def test_reference_strategies(self):
        """method for testing reference strategies"""
        content_object: Content = get_content(self.test_user, self.portfolio_id)[3]
        next_period(content_object)
        coordinate_reference_actions(content_object)
        do_nothing_cash = read_portfolio_content(self.portfolio_id + 1)[0][1]
        self.assertEqual(do_nothing_cash, INITIAL_CAPITAL)
        all_in_cash = read_portfolio_content(self.portfolio_id + 2)[0][1]
        self.assertAlmostEqual(all_in_cash, 0)
        even_content = read_portfolio_content(self.portfolio_id + 3)
        self.assertTrue(len(even_content) >= 19)

    def tearDown(self):
        delete_user_portfolios("testing")
        delete_user("testing")
