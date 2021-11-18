from services.user_services import login
from services.user_services import signup
from services.portfolio_services import create_portfolio
from services.portfolio_services import get_portfolios
from services.content_services import get_content
from services.content_services import buy
from services.content_services import sell
from services.content_services import next_period

'''Text UI for logging in'''
def login_UI():
    while True:
        username=input("Username: ")
        password=input("Password: ")
        print("-----------------")
        response=login(username, password)
        if response:
            return response


'''Text UI for signing up'''
def signup_UI():
    while True:
        username=input("Username: ")
        password=input("Password: ")
        response= signup(username, password)
        if response:
            return response
        else:
            print("Please try again.")
            print("---------------")


'''Text UI for listing the portfolios'''
def list_portfolios(user_id):
    print("Your portfolios:")
    portfolios=get_portfolios(user_id)
    for portfolio in portfolios:
        print (f"{portfolio[0]}: {portfolio[1]}")
    print("-----------------")


'''Text UI for creating a new portfolio'''
def create_portfolio_UI(user_id):
    portfolio_name=input("Name of the new portfolio: ")
    print("------------------")
    print("How often do you want to make investment decisions in this portfolio?")
    frequency = int (input("1: Daily, 2: Weekly or 3: Monthly. "))
    print("------------------")
    create_portfolio(user_id, portfolio_name, frequency)


'''Text UI for starting the application and controlling the flow'''
def start():
    #To do: add functionality for going backwards in the flow like this: contents -> portfolios -> users
    while True:
        response=input("press L to login, N to create a new user, Q to quit: ")
        print("--------------")
        if response=='L' or response=='l':
            user_id=login_UI()
            break
        if response=='N' or response=='n':
            user_id=signup_UI()
            break
        if response=='Q' or response=='q':
            exit()
    if user_id:
        while True:
            list_portfolios(user_id)
            response=input(("Press O to open a portfolios, C to create a new portfolio, Q to quit: "))
            if response=='O' or response=='o':
                portfolio_id=int(input("Number of portfolio to open: "))
                content_object=get_content(portfolio_id)
                break
            if response=='C' or response=='c':
                create_portfolio_UI(user_id)
            if response=='Q' or response=='q':
                print("------------------")
                exit()
    if content_object:
        while(True):
            print("What do you want to do next?")
            choice=input("Press B to buy, S to sell, N for next period, Q for quit: ")
            print("---------")
            if choice=='B' or choice=='b':
                crypto_id=int(input("Number of crypto to buy: "))
                investment=int(input("Amount to invest (EUR): "))
                buy(content_object, crypto_id, investment)
                get_content(portfolio_id)
            if choice=='S' or choice=='s':
                crypto_id=int(input("Which crypto do you want to sell? "))
                investment=int(input("How much do you want to sell in EUR? " ))
                sell(content_object, crypto_id, investment)
                get_content(portfolio_id)
            if choice=='N' or choice=='n':
                next_period(content_object)
                get_content(portfolio_id)
            if choice=='Q' or choice=='q':
                exit()


    
