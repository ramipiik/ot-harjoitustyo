
from repositories.portfolios import create_portfolio_repository
from repositories.portfolios import read_user_porftfolios_repository
from repositories.portfolios import read_portfolio_content
from repositories.portfolios import store_first_time
from repositories.portfolios import fetch_portfolio_id
from repositories.portfolios import store_contents

from repositories.read_prices import get_prices
from entities.portfolio import Portfolio
from entities.content import Content

FIRST_DAY='2020-01-01' #Later: Choose the start day randomly
INITIAL_CAPITAL=1000000

def create_portfolio_service(user_id, portfolio_name, frequency):
    if frequency==1:
        frequency='daily'
    if frequency==2:
        frequency='weekly'
    if frequency==3:
        frequency='monthly'

    new_portfolio = Portfolio(user_id, portfolio_name, frequency)
    create_portfolio_repository(user_id, new_portfolio)
    new_portfolio.id=fetch_portfolio_id(user_id, portfolio_name)
    content_object=first_day(new_portfolio, user_id)
    return content_object
    # create_porftfolio_repository(user_id, portfolio_name, frequency)

def get_portfolio_id(user_id, portfolio_name):
    return fetch_portfolio_id(user_id, portfolio_name)

def first_day(portfolio:Portfolio, user_id):
    # portfolio_id=fetch_portfolio_id(user_id, portfolio.name)
    # print("portfolio_id", portfolio_id)
    content_object=Content(store_first_time(portfolio, FIRST_DAY, INITIAL_CAPITAL))
    return content_object

def buy(content_object:Content, crypto_id, amount):
    content_object.buy(crypto_id, amount)
    store_contents(content_object)
    # self.cash-=investment
    # if currency in self.portfolio.keys():
    #     before=self.portfolio[currency][0] 
    #     after=before+investment/price 
    #     self.portfolio[currency]=[after, after*price] #[määrä, arvo]
    # else:
    #     self.portfolio[currency]=[investment/price, price]
    

def fetch_user_portfolios_service(user_id):
    return read_user_porftfolios_repository(user_id)

def fetch_portfolio_content(portfolio_id):
    print("checkpoint A")
    content=read_portfolio_content(portfolio_id)  
    date=content[0][0]
    cash=content[0][1]
    change_id=content[0][4]
    content_object=Content(portfolio_id, date, cash, change_id)

    print("---------")

    print("Date:", date)
    print("Cash:", cash)
    rates=get_prices(date)
    for row in content:
        if row[2]:
            print(row[2], rates[row[2]]["name"], row[3], "pieces")
            content_object.cryptos[row[2]]=row[3]
    print("---------")
    fetch_rates(date)
    return content_object
    

def fetch_rates(date):    
    print("Today's Rates")
    if date:
        rates=get_prices(date)
        aux=[]
        for key, value in rates.items():
            aux.append(key)
            print(f"{key}: {value['name']} {value['close']:.4f} EUR")
    print("-------------")
    # if date:
    #     rates=get_prices(date)
    #     for key, value in rates.items():
    #         print(f"{key} {value}")
    # exit()
    # for key, value in self.portfolio.items():
    #     price_of_the_day=rates[key]["close"]
    #     self.portfolio[key]=[self.portfolio[key][0], self.portfolio[key][0]*price_of_the_day]
    # return self.portfolio


# def list_portfolio_content(portfolio_id):
    # print(f"Starting capital: {user.portfolios[portfolio_name].get_cash()} EUR")