class Portfolio:
    """Class for managing portfolios"""

    def __init__(self, user_id, name, frequency, periods=None):
        self.frequency = frequency
        self.user_id = user_id
        self.name = name
        self.periods = periods
        self.id = None  # Created by database
