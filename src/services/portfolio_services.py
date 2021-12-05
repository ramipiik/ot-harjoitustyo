from repositories.portfolio_repository import (
    store_portfolio,
    read_portfolios,
    read_portfolio_id,
    read_reference_portfolios
)
from repositories.content_repository import store_content_first_time
from repositories.portfolio_repository import store_reference_portfolios
from entities.portfolio import Portfolio
from entities.reference_portfolio import Reference_Portfolio
from entities.content import Content
from entities.user import User


# To do: Choose the start day randomly
FIRST_DAY = "2020-06-01"
INITIAL_CAPITAL = 1000000

REFERENCE_STRATEGIES = [
    'do_nothing',
    'all-in',
    'even',
    'random',
    'follow',
    'contrarian'
]

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

    #vaihda järjestystä. Tallenna ensin tietokantaan
    
    store_reference_portfolios(new_portfolio.id, REFERENCE_STRATEGIES, frequency, None)
    reference_portfolios:dict=read_reference_portfolios(new_portfolio.id)    
    #print (reference_portfolios)
    for strategy, id in reference_portfolios.items():
        new_portfolio.reference_portfolios[strategy]=Reference_Portfolio(new_portfolio.id, strategy, frequency, id)
    
    for reference_portfolio in new_portfolio.reference_portfolios.values():
        # print(x, y.strategy, y.id)    
        store_content_first_time(reference_portfolio, FIRST_DAY, INITIAL_CAPITAL, True)

    # aux=store_content_first_time(reference_portfolio, FIRST_DAY, INITIAL_CAPITAL)
    
    return content_object


def get_portfolios(user):
    """Service for fetching user's portfolios"""
    portfolios = read_portfolios(user.username)
    return portfolios
