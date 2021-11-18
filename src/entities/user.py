
from .portfolio import Portfolio

# This class is currently not used.
# User data is directly stored to and read from the database.
# To do: keep the logged in user object in memory

'''Class for managing users'''
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.portfolios={}
    
    def add_portfolio(self, portfolio_name, frequency, periods):
        self.portfolios[portfolio_name]=Portfolio(frequency, periods)
     
