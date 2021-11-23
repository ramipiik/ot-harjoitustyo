from repositories.portfolio_repository import (
    store_portfolio,
    read_portfolios,
    read_portfolio_id,
)
from repositories.content_repository import store_content_first_time
from entities.portfolio import Portfolio
from entities.content import Content
from entities.user import User


# To do: Choose the start day randomly
FIRST_DAY = "2020-06-01"
INITIAL_CAPITAL = 1000000


def create_portfolio(user: User, portfolio_name, frequency):
    """Service for creating a new portfolio"""
    if frequency == 1:
        frequency = "daily"
    if frequency == 2:
        frequency = "weekly"
    if frequency == 3:
        frequency = "monthly"
    new_portfolio = Portfolio(user.username, portfolio_name, frequency)
    store_portfolio(user.username, new_portfolio)
    new_portfolio.id = read_portfolio_id(user.username, portfolio_name)
    aux = store_content_first_time(new_portfolio, FIRST_DAY, INITIAL_CAPITAL)
    content_object = Content(aux[0], aux[1], aux[2], aux[3])
    user.add_portfolio(new_portfolio.id)
    return content_object


def get_portfolios(user):
    """Service for fetching user's portfolios"""
    portfolios = read_portfolios(user.username)
    return portfolios
