import datetime

from repositories.content_repository import read_portfolio_content, store_content
from repositories.portfolio_repository import read_portfolio_frequency, read_reference_portfolios
from repositories.price_repository import read_prices, read_max_day
from services.price_services import get_rates
from services.portfolio_services import get_portfolios
from services.statistic_services import get_portfolio_statistics
from entities.content import Content
from ui.styles import ERROR_MESSAGE, bcolors
from entities.content import Content
from repositories.crypto_repository import read_crypto_ids



def buy(content_object: Content, crypto_id, investment):
    """Service for buying"""
    
    # if content_object.buy(crypto_id, investment):
    #     rates = read_prices(content_object.portfolio_day)
    #     store_content(content_object, rates)
    print("From buy service. Crypto_id", crypto_id)
    content_object.buy(crypto_id, investment)
    rates = read_prices(content_object.portfolio_day)
    store_content(content_object, rates)


def sell(content_object: Content, crypto_id, investment):
    """Service for selling"""
    if content_object.sell(crypto_id, investment):
        rates = read_prices(content_object.portfolio_day)
        store_content(content_object, rates)


def get_reference_content(portfolio_id, date):
    references:dict=read_reference_portfolios(portfolio_id)
    print(f"{bcolors.HEADER}Reference portfolios {date}")
    print("")
    for strategy, id in references.items():
        #content = read_portfolio_content(id)
        stats = get_portfolio_statistics(id)
        if stats["today"]:
            print(
                f"{strategy}: {stats['today']}€ | d {stats['d']}% | w {stats['w']}% | m {stats['m']}% | y {stats['y']}% | sd {stats['vol']}%")       
    print(f"--------------{bcolors.ENDC}")

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
    print(f"Your portfolio {date}")
    print("Cash:", cash, "EUR")
    rates = read_prices(date)
    for row in content:
        if row[2]:
            print(f"{row[2]} ({rates[row[2]]['name']}): {row[5]:.0f} EUR")
            content_object.cryptos[row[2]] = {}
            content_object.cryptos[row[2]]["amount"] = row[3]
            content_object.cryptos[row[2]]["value"] = row[5]
    print("")
    stats = get_portfolio_statistics(portfolio_id)
    if stats["today"]:
        print(
            f"Portfolio value: {stats['today']}€ | d {stats['d']}% | w {stats['w']}% | m {stats['m']}% | y {stats['y']}% | sd {stats['vol']}%")
    print(f"--------------------{bcolors.ENDC}")
    get_reference_content(portfolio_id, date)
    get_rates(date)
    return content_object


def next_period(content_object: Content):
    """Service for starting the next period"""
    
    do_reference_actions(content_object)
    max_day = read_max_day()[0]
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

    for i in range(days):
        # print ("i", i)
        date_object += datetime.timedelta(1)
        if date_object > max_day_object:
            print(f"{bcolors.FAIL}No more price data available.")
            date_object -= datetime.timedelta(days)
            break
        
        content_object.portfolio_day = str(date_object)
        content_object.change_id += 1
        rates = read_prices(str(date_object))
        store_content(content_object, rates)

        portfolio_id=content_object.portfolio_id
        refs:dict=read_reference_portfolios(portfolio_id)
        for key,ref_portfolio_id in refs.items():
            content=read_portfolio_content(ref_portfolio_id)
            cash=content[0][1]
            change_id=content[0][4]    
            ref_content_object=Content(ref_portfolio_id, content_object.portfolio_day, cash, change_id)
            ref_content_object.change_id += 1
            ref_content_object.cryptos= {}
            # print("content")
            # print(content)
            for row in content:
                print(row)
                crypto_id=row[2]
                crypto_amount=row[3]
                crypto_value=row[4]
                ref_content_object.cryptos[crypto_id]={}
                if crypto_id:
                    ref_content_object.cryptos[crypto_id]["amount"]=crypto_amount
                    ref_content_object.cryptos[crypto_id]["value"]=crypto_value
            store_content(ref_content_object, rates)


def do_reference_actions(content_object:Content):
    portfolio_id=content_object.portfolio_id
    refs:dict=read_reference_portfolios(portfolio_id)
    for key,ref_portfolio_id in refs.items():
        content=read_portfolio_content(ref_portfolio_id)
        cash=content[0][1]
        change_id=content[0][4]
        print("cash", cash)
        ref_content_object=Content(ref_portfolio_id, content_object.portfolio_day, cash, change_id)
        print("ref_content_object.cash", ref_content_object.cash)
        if key=='do_nothing':
            print("This one is easy")
        if key=='all-in':
            if cash>1:
                crypto_ids=read_crypto_ids()
                nr_of_cryptos=len(crypto_ids)
                investment_amount=cash/nr_of_cryptos
                print("investment_amount", investment_amount)
                for crypto_id in crypto_ids:
                    print(crypto_id)
                    buy(ref_content_object, crypto_id, investment_amount)
        # print(key, value)
