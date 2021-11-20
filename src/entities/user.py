from .portfolio import Portfolio

# This class is currently not used.
# User data is directly stored to and read from the database.
# To do: keep the logged in user object in memory


class User:
    """Class for managing users"""

    def __init__(self, id, username, is_admin):
        self.id = id
        self.username = username
        self.is_admin = is_admin
        self.portfolios = []

    def add_portfolio(self, portfolio_id):
        self.portfolios.append(portfolio_id)

    def get_porffolios(self):
        return self.portfolios
