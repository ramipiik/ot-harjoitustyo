class ReferencePortfolio:
    """Class for managing reference_portfolios"""

    def __init__(self, portfolio_id, strategy, frequency, id, periods=None):
        self.frequency = frequency
        self.portfolio_id = portfolio_id
        self.strategy = strategy
        self.periods = periods
        self.id = id
