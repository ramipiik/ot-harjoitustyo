class User:
    """Class for managing users"""

    def __init__(self, user_id, username, is_admin):
        self.id = user_id
        self.username = username
        self.is_admin = is_admin
        self.portfolios = []

    def add_portfolio(self, portfolio_id):
        self.portfolios.append(portfolio_id)

    def get_porffolios(self):
        return self.portfolios
