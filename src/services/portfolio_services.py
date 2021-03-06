from repositories.portfolio_repository import (
    store_portfolio,
    read_portfolios,
    read_portfolio_id,
    read_reference_portfolios,
)
from repositories.content_repository import store_content_first_time
from repositories.portfolio_repository import store_reference_portfolios
from entities.portfolio import Portfolio
from entities.reference_portfolio import ReferencePortfolio
from entities.content import Content
from entities.user import User


# To do: Choose the start day randomly
FIRST_DAY = "2020-06-01"
INITIAL_CAPITAL = 1000000

REFERENCE_STRATEGIES = [
    "Do nothing",
    "All-in",
    "Even",
    "Random",
    "Follow",
    "Contrarian",
]


def number_to_frequency(frequency_number):
    """
    Helper function for converting frequency number to string

    Args:
        frequency_number (int): 1, 7 or 30

    Returns:
        string: 'daily', 'weekly' or 'monthly'
    """
    if frequency_number == 1:
        return "daily"
    if frequency_number == 2:
        return "weekly"
    if frequency_number == 3:
        return "monthly"


def create_portfolio(user: User, portfolio_name, frequency_number):
    """
    Service for creating a new portfolio

    Args:
        user (User): User for whom the portfolio is created
        portfolio_name (str): Name of the new portfolio
        frequency_number (int): Decision making frequency

    Returns:
        Content: Content of the new portfolio
    """
    frequency = number_to_frequency(frequency_number)
    new_portfolio = Portfolio(user.username, portfolio_name, frequency)
    store_portfolio(user.username, new_portfolio)
    new_portfolio.id = read_portfolio_id(user.username, portfolio_name)
    aux = store_content_first_time(new_portfolio, FIRST_DAY, INITIAL_CAPITAL)
    content_object = Content(aux[0], aux[1], aux[2], aux[3])
    user.add_portfolio(new_portfolio.id)
    store_reference_portfolios(
        new_portfolio.id, REFERENCE_STRATEGIES, frequency, None)
    reference_portfolios: dict = read_reference_portfolios(new_portfolio.id)
    for strategy, id in reference_portfolios.items():
        new_portfolio.reference_portfolios[strategy] = ReferencePortfolio(
            new_portfolio.id, strategy, frequency, id
        )
    for reference_portfolio in new_portfolio.reference_portfolios.values():
        store_content_first_time(
            reference_portfolio, FIRST_DAY, INITIAL_CAPITAL)
    return content_object


def get_portfolios(user):
    """
    Service for fetching user's portfolios

    Args:
        user (User): User whole portfolios are fetched

    Returns:
        list: List of lists containing portfolio id and portfolio name ordered by id
    """
    portfolios = read_portfolios(user.username)
    return portfolios
