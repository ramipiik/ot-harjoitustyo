import datetime

from repositories.content_repository import read_portfolio_content, store_content
from repositories.portfolio_repository import read_portfolio_frequency
from repositories.price_repository import read_prices, read_max_day
from services.price_services import get_rates
from services.portfolio_services import get_portfolios
from entities.content import Content
from ui.styles import ERROR_MESSAGE, bcolors


def buy(content_object: Content, crypto_id, investment):
    """Service for buying"""
    if content_object.buy(crypto_id, investment):
        rates = read_prices(content_object.portfolio_day)
        store_content(content_object, rates)


def sell(content_object: Content, crypto_id, investment):
    """Service for selling"""
    if content_object.sell(crypto_id, investment):
        rates = read_prices(content_object.portfolio_day)
        store_content(content_object, rates)


def get_content(user, portfolio_id):
    """Service for fetching and printing portfolio content. Returns a content object."""
    portfolios = []
    aux = get_portfolios(user)
    for item in aux:
        portfolios.append(item[0])
    if portfolio_id not in portfolios:
        print(ERROR_MESSAGE)
        return False
    content = read_portfolio_content(portfolio_id)
    date = content[0][0]
    cash = content[0][1]
    change_id = content[0][4]
    content_object = Content(portfolio_id, date, cash, change_id)

    # To do: Move prints to text UI?
    print(f"{bcolors.OKGREEN}--------------------")
    print(f"Portfolio content {date}")
    print("Cash:", cash, "EUR")
    rates = read_prices(date)
    for row in content:
        if row[2]:
            print(f"{row[2]} ({rates[row[2]]['name']}): {row[5]:.0f} EUR")
            content_object.cryptos[row[2]] = {}
            content_object.cryptos[row[2]]["amount"] = row[3]
            content_object.cryptos[row[2]]["value"] = row[5]
    print("")
    if content[0][6]:
        print(f"Total value: {content[0][6]:.0f} EUR")
    print(f"--------------------{bcolors.ENDC}")
    get_rates(date)
    return content_object


def next_period(content_object: Content):
    """Service for starting the next period"""
    max_day=read_max_day()[0]
    date = content_object.portfolio_day
    frequency = read_portfolio_frequency(content_object.portfolio_id)[0]
    if frequency == "daily":
        days = 1
    elif frequency == "weekly":
        days = 7
    elif frequency == "monthly":
        days = 30
    date_object = datetime.datetime(
        int(date[0:4]), int(date[5:7]), int(date[8:10])
    ).date()
    
    max_day_object = datetime.datetime(
        int(max_day[0:4]), int(max_day[5:7]), int(max_day[8:10])
    ).date()

    date_object += datetime.timedelta(days)
    if date_object>max_day_object:
        print(f"{bcolors.FAIL}No more price data available.")
        date_object -= datetime.timedelta(days)
    content_object.portfolio_day = str(date_object)
    content_object.change_id += 1
    rates = read_prices(str(date_object))
    store_content(content_object, rates)
