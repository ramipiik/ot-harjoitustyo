class User:
    """Class for managing users"""

    def __init__(self, user_id, username, is_admin):
        self.id = user_id
        self.username = username
        self.is_admin = is_admin
        self.portfolios = []

    def add_portfolio(self, portfolio_id):
        """
        Attaches a new portfolio to the user

        Args:
            portfolio_id: id number of the portfolio to add
        """
        self.portfolios.append(portfolio_id)

    def get_porffolios(self):
        """
        Returns user's portfolios

        Returns:
            List of portfolios
        """
        return self.portfolios
