import datetime
from repositories.read_prices import get_prices


def flow (portfolio):
    print("flow")
    first_year=2021
    first_month=10
    first_day=1
    date = datetime.datetime(first_year, first_month, first_day).date()
    i=1
    while i<=portfolio.periods:
        print("----------------------")
        print("Rates after day",i)
        print("")
        rates=get_prices(date)
        n=1
        aux=[]
        for key, value in rates.items():
            aux.append(key)
            print(f"{n} {key}: {value['close']:.4f} EUR")
            n+=1

        while (True):
            print("----------------------")
            print("Your portfolio")
            print("Cash: ", portfolio.get_cash(), "EUR")
            portfolio_content:dict=portfolio.get_portfolio(date)
            for key, value in portfolio_content.items():
                print(f"{key}: {value[1]:.2f} EUR")
            print("----------------------")
            print("What do you want to do?")
            print("0: Nothing")
            print("1: Buy")
            print("2: Sell")
            print("----------------------")
            choice=int(input())
            if choice==0:
                break
            if choice==1:
                print("What currency do you want to buy?")
                choice=int(input())
                currency=aux[choice-1]
                print("How much do you want to invest?")
                amount=int(input())
                portfolio.buy(currency, rates[currency]["close"], amount)
            if choice==2:
                print("Which currency do you want to sell?")
                currency=input()
                print("How much do you want to sell in EUR?")
                amount=int(input())
                portfolio.sell(currency, rates[currency]["close"], amount)
        date += datetime.timedelta(days=1)
        i+=1
        

        
