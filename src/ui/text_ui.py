
from entities.user import User
from entities.portfolio import Portfolio
from services.user_services import login_service
from services.user_services import signup_service
from services.portfolio_services import create_portfolio_service
from services.portfolio_services import fetch_user_portfolios_service
from services.portfolio_services import fetch_portfolio_content
from services.portfolio_services import buy

def login():
    while True:
        username=input("Username: ")
        password=input("Password: ")
        response=login_service(username, password)
        if response:
            return response

def signup():
    username=input("Username: ")
    password=input("Password: ")
    signup_service(username, password)

def list_portfolios(user_id):
    print("Your portfolios:")
    portfolios=fetch_user_portfolios_service(user_id)
    for portfolio in portfolios:
        print (f"Id: {portfolio[0]}: {portfolio[1]}")

def open_portfolio(portfolio_id):
    content=fetch_portfolio_content(portfolio_id)
    return content
    # print(content)

def create_portfolio(user_id):
    portfolio_name=input("Name of the new portfolio: ")
    print("How often do you want to make investment decisions in this portfolio?")
    frequency = int (input("1: Daily, 2: Weekly or 3: Monthly. "))
    create_portfolio_service(user_id, portfolio_name, frequency)

def start():
    while True:
        print("press L to login, N to create a new user, Q to quit")
        response=input()
        if response=='L' or response=='l':
            user_id=login()
            break
        if response=='N' or response=='n':
            user_id=signup()
            break
        if response=='Q' or response=='q':
            exit()
    if user_id:
        while True:
            list_portfolios(user_id)
            print("Press O to open one of the existing portfolios, C to create a new portfolio, Q to quit")
            response=input()
            if response=='O' or response=='o':
                portfolio_id=int(input("Which portfolio do you want to open? "))
                content_object=open_portfolio(portfolio_id)
                print("checkpoint 1")
                break
            if response=='C' or response=='c':
                content_object=create_portfolio(user_id)
            if response=='Q' or response=='q':
                exit()
    if portfolio_id:
        while(True):
            print("Awesome!")
            print("What do you want to do next?")
            print("Press B to buy, S to sell, N for next day, Q for save and quit")
            choice=input()
            if choice=='B' or choice=='b':
                print("What currency do you want to buy?")
                crypto_id=int(input())
                print("How much do you want to invest?")
                amount=int(input())
                buy(content_object, crypto_id, amount)
                fetch_portfolio_content(portfolio_id)
            if choice==2:
                print("Which currency do you want to sell?")
                currency=input()
                print("How much do you want to sell in EUR?")
                amount=int(input())
                portfolio.sell(currency, rates[currency]["close"], amount)


    
