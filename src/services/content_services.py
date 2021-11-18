import datetime

from repositories.content_repository import read_portfolio_content
from repositories.content_repository import store_content
from repositories.portfolio_repository import read_portfolio_frequency
from repositories.price_repository import read_prices
from services.price_services import get_rates
from entities.content import Content


'''Service for buying'''
def buy(content_object:Content, crypto_id, investment):
    content_object.buy(crypto_id, investment)
    rates=read_prices(content_object.portfolio_day)
    store_content(content_object, rates)


'''Service for selling'''
def sell(content_object:Content, crypto_id, investment):
    content_object.sell(crypto_id, investment)
    rates=read_prices(content_object.portfolio_day)
    store_content(content_object, rates)


'''Service for fetching and printing portfolio content. Returns a content object.'''
def get_content(portfolio_id):
    # To-do: Add a check for checking the logged-in user. Currently the method opens any portfolio regardless of the user if one guesses the number.
    # -> Need to keep the logged-in user in memory (currently missing)..
    content=read_portfolio_content(portfolio_id)  
    date=content[0][0]
    cash=content[0][1]
    change_id=content[0][4]
    content_object=Content(portfolio_id, date, cash, change_id)
    
    #To do: Move prints to text UI?
    print("---------")
    print(f"Portfolio content {date}")
    print("")
    print("Cash:", cash, "EUR")
    rates=read_prices(date)
    for row in content:
        if row[2]:
            print(f"{row[2]} ({rates[row[2]]['name']}): {row[5]:.0f} EUR")
            content_object.cryptos[row[2]]={}
            content_object.cryptos[row[2]]["amount"]=row[3]
            content_object.cryptos[row[2]]["value"]=row[5]
    print("")
    if content[0][6]:
        print(f"Total value: {content[0][6]:.0f} EUR")
    print("---------")
    get_rates(date)
    return content_object


'''Service for starting the next period'''
def next_period(content_object:Content):
    date=content_object.portfolio_day
    frequency=(read_portfolio_frequency(content_object.portfolio_id)[0])
    if frequency=='daily':
        n=1
    elif frequency=='weekly':
        n=7
    elif frequency=='monthly':
        n=30
    date_object = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10])).date()
    date_object += datetime.timedelta(days=n)
    content_object.portfolio_day=str(date_object)
    content_object.change_id+=1
    rates=read_prices(str(date_object))
    store_content(content_object, rates)