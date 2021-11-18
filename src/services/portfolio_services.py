from repositories.portfolio_repository import store_portfolio
from repositories.portfolio_repository import read_portfolios
from repositories.content_repository import store_content_first_time
from repositories.portfolio_repository import read_portfolio_id
from entities.portfolio import Portfolio
from entities.content import Content


#To do: Choose the start day randomly
FIRST_DAY='2020-01-01'
INITIAL_CAPITAL=1000000


'''Service for creating a new portfolio'''
def create_portfolio (user_id, portfolio_name, frequency):
    if frequency==1:
        frequency='daily'
    if frequency==2:
        frequency='weekly'
    if frequency==3:
        frequency='monthly'
    new_portfolio = Portfolio(user_id, portfolio_name, frequency)
    store_portfolio(user_id, new_portfolio)
    new_portfolio.id=read_portfolio_id(user_id, portfolio_name)
    aux=store_content_first_time(new_portfolio, FIRST_DAY, INITIAL_CAPITAL)
    content_object=Content(aux[0], aux[1], aux[2], aux[3])
    return content_object


'''Service for fetching user's portfolios'''
def get_portfolios(user_id):
    return read_portfolios(user_id)
