from services.user_services import login, signup
from services.portfolio_services import create_portfolio, get_portfolios
from services.content_services import get_content, buy, sell, next_period
from ui.styles import bcolors, ERROR_MESSAGE

"""Text UI for logging in"""
def login_UI():
    while True:
        username = input(f"{bcolors.OKCYAN}Username: {bcolors.ENDC}")
        password = input(f"{bcolors.OKCYAN}Password: {bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}--------------------{bcolors.ENDC}")
        response = login(username, password)
        if response:
            return response


"""Text UI for signing up"""
def signup_UI():
    while True:
        username = input(f"{bcolors.OKCYAN}Username: {bcolors.ENDC}")
        password = input(f"{bcolors.OKCYAN}Password: {bcolors.ENDC}")
        response = signup(username, password)
        if response:
            return response
        else:          
            print(f"{bcolors.FAIL}Please try again.{bcolors.ENDC}")
            print(f"{bcolors.FAIL}--------------------{bcolors.ENDC}")
            {bcolors.ENDC}
            

"""Text UI for listing the portfolios"""
def list_portfolios(user_id):
    print(f"{bcolors.OKBLUE}Your portfolios:")
    portfolios = get_portfolios(user_id)
    for portfolio in portfolios:
        print(f"{portfolio[0]}: {portfolio[1]}")
    print(f"--------------------{bcolors.ENDC}")


def create_portfolio_UI(user_id):
    """Text UI for creating a new portfolio"""
    portfolio_name = input(f"{bcolors.OKCYAN}Name of the new portfolio: {bcolors.ENDC}")
    while True:
        print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}How often do you want to make investment decisions in this portfolio?{bcolors.ENDC}")
        try:
            frequency = int(input(f"{bcolors.OKCYAN}1: Daily, 2: Weekly or 3: Monthly. {bcolors.ENDC}"))
        except:
            print(ERROR_MESSAGE)
            continue
        if frequency not in [1,2,3,]:
            print(ERROR_MESSAGE)
            continue
        break

    print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
    create_portfolio(user_id, portfolio_name, frequency)



def start():
    """Text UI for starting the application and controlling the flow"""
    # To do: add functionality for going backwards in the flow like this: contents -> portfolios -> users
    while True:
        response = input(f"{bcolors.OKCYAN}press L to login, N to create a new user, Q to quit: {bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
        if response == "L" or response == "l":
            user_id = login_UI()
            break
        if response == "N" or response == "n":
            user_id = signup_UI()
            break
        if response == "Q" or response == "q":
            exit()
        print(ERROR_MESSAGE)
    if user_id:
        while True:
            list_portfolios(user_id)
            response = input(
                (
                    f"{bcolors.OKCYAN}Press O to open a portfolios, C to create a new portfolio, Q to quit: {bcolors.ENDC}"
                )
            )
            if response == "O" or response == "o":
                try: 
                    portfolio_id = int(input(f"{bcolors.OKCYAN}Number of portfolio to open: {bcolors.ENDC}"))
                    content_object = get_content(portfolio_id)
                    break
                except:
                    print(ERROR_MESSAGE)
            elif response == "C" or response == "c":
                create_portfolio_UI(user_id)
            elif response == "Q" or response == "q":
                print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
                exit()
            else:
                print(ERROR_MESSAGE)
    if content_object:
        while True:
            print(f"{bcolors.OKCYAN}What do you want to do next?{bcolors.ENDC}")
            choice = input(f"{bcolors.OKCYAN}Press B to buy, S to sell, N for next period, Q for quit: {bcolors.ENDC}")
            print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
            if choice == "B" or choice == "b":
                try:
                    crypto_id = int(input(f"{bcolors.OKCYAN}Number of crypto to buy: {bcolors.ENDC}"))
                    investment = int(input(f"{bcolors.OKCYAN}Amount to invest (EUR): {bcolors.ENDC}"))
                except:
                    print(ERROR_MESSAGE)
                buy(content_object, crypto_id, investment)
                get_content(portfolio_id)
            elif choice == "S" or choice == "s":
                try:
                    crypto_id = int(input(f"{bcolors.OKCYAN}Which crypto do you want to sell? {bcolors.ENDC}"))
                    investment = int(input(f"{bcolors.OKCYAN}How much do you want to sell in EUR? {bcolors.ENDC}"))
                except:
                    print(ERROR_MESSAGE)
                sell(content_object, crypto_id, investment)
                get_content(portfolio_id)
            elif choice == "N" or choice == "n":
                next_period(content_object)
                get_content(portfolio_id)
            elif choice == "Q" or choice == "q":
                exit()
            else: 
                print(ERROR_MESSAGE)
