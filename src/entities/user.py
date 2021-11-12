from .portfolio import Portfolio

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.portfolios={}
    
    def add_portfolio(self, portfolio_name, frequency, periods):
        self.portfolios[portfolio_name]=Portfolio(frequency, periods)
     
