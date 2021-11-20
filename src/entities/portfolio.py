class Portfolio:
    """Class for managing portfolios"""

    def __init__(self, username, name, frequency, periods=None):
        self.frequency = frequency
        self.username = username
        self.name = name
        self.periods = periods
        self.id = None  # Created by database
