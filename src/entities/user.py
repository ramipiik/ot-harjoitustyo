# Hmm... The very first version, which didn't have a database connection, was using the User object below
# However, after adding the database connection, I discovered that I didn't anymore use the Classes at all.
# Somehow the SQL structure sneakily started dominating over the object oriented structure of Python, and now I'm not using the objects at all.
# How does one balance relational database schema and object oriented programming?
# I know there are some Python-SQlite ORM libraries, but to me it feels that they  add a lot of complexity in the code in exchange for not having to write the SQL queries.
# However, to me it makes more sense to work directly with the SQL queries than with the absracttion layer.
# But in this case it led to me totally dropping the entities.
# Could you please comment? What am I missing?

from .portfolio import Portfolio

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.portfolios={}
    
    def add_portfolio(self, portfolio_name, frequency, periods):
        self.portfolios[portfolio_name]=Portfolio(frequency, periods)
     
