
from entities.user import User
from entities.portfolio import Portfolio
def start():
    username='rami'
    password='xxx'
    user=User(username, password)
    print("Create a new portfolio")
    portfolio_name=input("Name of the portfolio: ")
    print("How often do you want to make investment decisions in this portfolio?")
    print ("1: Daily, 2: Weekly or 3: Monthly")
    frequency = int(input())
    print("-----------")
    print("How many such periods do you want to simulate")
    periods=int(input())
    print("----------------")
    user.add_portfolio(portfolio_name, frequency, periods)
    print(f"Starting capital: {user.portfolios[portfolio_name].get_cash()} EUR")
    print("----------------")
    
    return (user.portfolios[portfolio_name])
