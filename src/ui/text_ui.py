from sqlite3.dbapi2 import Error
from services.user_services import login, signup
from services.portfolio_services import create_portfolio, get_portfolios
from services.content_services import get_content, buy, sell, next_period, get_date
from services.statistic_services import get_portfolio_statistics
from ui.styles import bcolors, ERROR_MESSAGE


def start_UI():
    """Text UI for starting the application and controlling the flow"""
    while True:
        response = input(
            f"{bcolors.OKCYAN}press L to login, N to create a new user, Q to quit: {bcolors.ENDC}"
        )
        print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
        if response == "L" or response == "l":
            user = login_UI()
            open_portfolio_UI(user)
        if response == "N" or response == "n":
            user = signup_UI()
            open_portfolio_UI(user)
        if response == "Q" or response == "q":
            exit()
        print(ERROR_MESSAGE)


def login_UI():
    """Text UI for logging in"""
    while True:
        username = input(f"{bcolors.OKCYAN}Username: {bcolors.ENDC}")
        password = input(f"{bcolors.OKCYAN}Password: {bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}--------------------{bcolors.ENDC}")
        user = login(username, password)
        if user:
            return user


def signup_UI():
    """Text UI for signing up"""
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


def list_portfolios_UI(user):
    """Text UI for listing the portfolios"""
    print(f"{bcolors.OKBLUE}Your portfolios:")
    portfolios = get_portfolios(user)
    for portfolio in portfolios:
        print(f"{portfolio[0]}: {portfolio[1]}")
    print(f"--------------------{bcolors.ENDC}")


def create_portfolio_UI(user):
    """Text UI for creating a new portfolio"""
    portfolio_name = input(f"{bcolors.OKCYAN}Name of the new portfolio: {bcolors.ENDC}")
    while True:
        print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
        print(
            f"{bcolors.OKCYAN}How often do you want to make investment decisions in this portfolio?{bcolors.ENDC}"
        )
        try:
            frequency = int(
                input(
                    f"{bcolors.OKCYAN}1: Daily, 2: Weekly or 3: Monthly. {bcolors.ENDC}"
                )
            )
        except:
            print(ERROR_MESSAGE)
            continue
        if frequency not in [
            1,
            2,
            3,
        ]:
            print(ERROR_MESSAGE)
            continue
        break
    print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
    create_portfolio(user, portfolio_name, frequency)

def logout_UI(user):
    old_username=user.username
    user=None
    print(f"{bcolors.OKCYAN}------------------")
    print(f"{old_username} logged out")
    print(f"------------------{bcolors.ENDC}")
    start_UI()

def open_portfolio_UI(user):
    while True:
        if user:
            while True:
                list_portfolios_UI(user)
                response = input(
                    (
                        f"{bcolors.OKCYAN}Which portfolio number do you want to open? C to create a new portfolio. X to logout. Q to quit: {bcolors.ENDC}"
                    )
                )
                if response == "C" or response == "c":
                    create_portfolio_UI(user)
                elif response == "Q" or response == "q":
                    print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
                    exit()
                elif response == "X" or response == "x":
                    logout_UI(user)
                else:
                    try:
                        portfolio_id = int(response)
                        response = get_content(user, portfolio_id)
                        content_object=response[3]
                        if content_object:
                            print_status(response)
                            break
                    except:
                        print(ERROR_MESSAGE)

        if content_object:
            action_UI(content_object, user, portfolio_id)
            

def action_UI(content_object, user, portfolio_id):
    while True:
        print(f"{bcolors.OKCYAN}What do you want to do next?{bcolors.ENDC}")
        choice = input(
            f"{bcolors.OKCYAN}Press B to buy, S to sell, N for next period, P back to Portfolio list, X to logout, Q for quit: {bcolors.ENDC}"
        )
        print(f"{bcolors.OKCYAN}------------------{bcolors.ENDC}")
        if choice == "B" or choice == "b":
            buy_ui(content_object, user, portfolio_id)
        elif choice == "S" or choice == "s":
            sell_ui(content_object, user, portfolio_id)
        elif choice == "N" or choice == "n":
            next_period(content_object)
            response=get_content(user, portfolio_id)
            print_status(response)
        elif choice == "Q" or choice == "q":
            exit()
        elif choice == "P" or choice == "p":
            break
        elif choice == "X" or choice == "x":
            logout_UI(user)
        else:
            print(ERROR_MESSAGE)


def sell_ui(content_object, user, portfolio_id):
    try:
        crypto_id = int(
            input(
                f"{bcolors.OKCYAN}Which crypto do you want to sell? {bcolors.ENDC}"
            )
        )
        investment = int(
            input(
                f"{bcolors.OKCYAN}How much do you want to sell in EUR? {bcolors.ENDC}"
            )
        )
        response=sell(content_object, crypto_id, investment)
        if type(response)==tuple and response[0]==False:
            print(f"{bcolors.FAIL}--------------------")
            print(response[1])
            print(f"--------------------{bcolors.ENDC}")
        response=get_content(user, portfolio_id)
        print_status(response)
    except:
        print(ERROR_MESSAGE)


def buy_ui(content_object, user, portfolio_id):
    try:
        crypto_id = int(
            input(
                f"{bcolors.OKCYAN}Number of crypto to buy: {bcolors.ENDC}"
            )
        )
        investment = int(
            input(
                f"{bcolors.OKCYAN}Amount to invest (EUR): {bcolors.ENDC}"
            )
        )   
        response=buy(content_object, crypto_id, investment)
        if type(response)==tuple and response[0]==False:
            print(f"{bcolors.FAIL}--------------------")
            print(response[1])
            print(f"--------------------{bcolors.ENDC}")
        response=get_content(user, portfolio_id)
        print_status(response)
    except:
        print(ERROR_MESSAGE)


def print_date(date):
    print(f"{bcolors.OKGREEN}--------------------")
    print("Portfolio", date)
    print("")


def print_stats(stats):
    if stats["today"]:
        print(
            f"Value: {stats['today']}€ ({stats['all-time']}%) | d {stats['d']}% | w {stats['w']}% | m {stats['m']}% | y {stats['y']}% | sd {stats['sd']}%"
        )


def print_cash(cash):
    print(" -Cash:", cash, "EUR")


def print_content(content, content_object, rates):
    for row in content:
        if row[2]:
            print(f" -{row[2]} ({rates[row[2]]['name']}): {row[5]:.0f} EUR")
            content_object.cryptos[row[2]] = {}
            content_object.cryptos[row[2]]["amount"] = row[3]
            content_object.cryptos[row[2]]["value"] = row[5]
    print(f"--------------------{bcolors.ENDC}")


def print_rates(rates, date):
    print(f"{bcolors.WARNING}Rates {date}")
    print("")
    aux = []
    for key, value in rates.items():
        aux.append(key)
        print(
            f"{key} ({value['name']}): {value['close']} | d {value['d']}% | w {value['w']}% | m {value['m']}% | y {value['y']}% | sd {value['sd']}%"
        )
    print(f"--------------------{bcolors.ENDC}")


def print_ranking(references, date):
    print(f"{bcolors.HEADER}Ranking {date}")
    print("")
    for i, strategy in enumerate(references):
        stats = get_portfolio_statistics(strategy[1])
        print(
            f"{i+1}. {strategy[0]}: {stats['today']}€ ({stats['all-time']}%) | d {stats['d']}% | w {stats['w']}% | m {stats['m']}% | y {stats['y']}% | sd {stats['sd']}%"
        )
    print(f"--------------{bcolors.ENDC}")


def print_status(response):
    date=response[0]
    cash=response[1]
    content=response[2]
    content_object = response[3]
    rates=response[4]
    stats=response[5]
    references=response[6]
    if content_object:
        print_date(date)
        print_stats(stats)
        print_cash(cash)
        print_content(content, content_object, rates)
        print_ranking(references, date)
        print_rates(rates, date)


