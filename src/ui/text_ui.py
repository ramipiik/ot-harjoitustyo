
from entities.user import User
from entities.portfolio import Portfolio
from services.user_services import login_service
from services.user_services import signup_service
from services.portfolio_services import create_portfolio_service
from services.portfolio_services import fetch_user_portfolios_service
from services.portfolio_services import fetch_portfolio_content
from services.portfolio_services import buy
from services.portfolio_services import sell
from services.portfolio_services import next_day

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
    return signup_service(username, password)

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
                ####Katso mitä tämä palauttaa!!!
                content_object=open_portfolio(portfolio_id)
                print("checkpoint 1")
                break
            if response=='C' or response=='c':
                create_portfolio(user_id)
            if response=='Q' or response=='q':
                exit()
    if content_object:
        while(True):
            print("Day", content_object.portfolio_day)
            print("What do you want to do next?")
            print("Press B to buy, S to sell, N for next day, Q for quit")
            choice=input()
            if choice=='B' or choice=='b':
                print("Which crypto do you want to buy?")
                crypto_id=int(input())
                print("How much do you want to invest?")
                investment=int(input())
                buy(content_object, crypto_id, investment)
                fetch_portfolio_content(portfolio_id)
            if choice=='S' or choice=='s':
                print("Which crypto do you want to sell?")
                crypto_id=int(input())
                print("How much do you want to sell in EUR?")
                investment=int(input())
                sell(content_object, crypto_id, investment)
                fetch_portfolio_content(portfolio_id)
            if choice=='N' or choice=='n':
                next_day(content_object)
                fetch_portfolio_content(portfolio_id)
            if choice=='Q' or choice=='q':
                exit()


    
