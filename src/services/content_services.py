import datetime
import random

from repositories.content_repository import (
    read_portfolio_content,
    store_content,
    read_portfolio_startdate
)
from repositories.portfolio_repository import (
    read_portfolio_frequency,
    read_reference_portfolios,
)
from repositories.price_repository import read_prices, read_max_day
from repositories.crypto_repository import read_crypto_names_and_ids
from services.price_services import get_rates
from services.portfolio_services import get_portfolios
from services.statistic_services import get_portfolio_statistics
from entities.content import Content
from ui.styles import ERROR_MESSAGE, bcolors


CRYPTO_NAMES_AND_IDS = read_crypto_names_and_ids()
CRYPTO_IDS = []
for key in CRYPTO_NAMES_AND_IDS:
    CRYPTO_IDS.append(key)
NR_OF_CRYPTOS = len(CRYPTO_IDS)


def buy(content_object: Content, crypto_id, investment):
    """Service for buying"""
    response=content_object.buy(crypto_id, investment)
    if type(response)==tuple and response[0]==False:
        return response
    if response:
        rates = read_prices(content_object.portfolio_day)
        store_content(content_object, rates)
      


def sell(content_object: Content, crypto_id, investment):
    """Service for selling. Allows short selling."""
    if content_object.sell(crypto_id, investment):
        rates = read_prices(content_object.portfolio_day)
        store_content(content_object, rates)


def get_reference_content(portfolio_id, date, own_portfolio_value, own_portfolio_id):
    """Service for ordering and printing reference portfolio valuations"""
    references: dict = read_reference_portfolios(portfolio_id)
    print(f"{bcolors.HEADER}Ranking {date}")
    print("")
    collection = []
    collection.append((own_portfolio_value, "Your portfolio", own_portfolio_id))
    for strategy, id in references.items():
        stats = get_portfolio_statistics(id)
        collection.append((stats["today"], strategy, id))
    collection.sort(reverse=True)
    ordered = []
    for item in collection:
        ordered.append((item[1], item[2]))
    for i, strategy in enumerate(ordered):
        stats = get_portfolio_statistics(strategy[1])
        print(
            f"{i+1}. {strategy[0]}: {stats['today']}€ ({stats['all-time']}%) | d {stats['d']}% | w {stats['w']}% | m {stats['m']}% | y {stats['y']}% | sd {stats['sd']}%"
        )
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
    print(f"{bcolors.OKGREEN}--------------------")
    print("Portfolio date", date)
    print("")
    stats = get_portfolio_statistics(portfolio_id)
    if stats["today"]:
        print(
            f"Value: {stats['today']}€ ({stats['all-time']}%) | d {stats['d']}% | w {stats['w']}% | m {stats['m']}% | y {stats['y']}% | sd {stats['sd']}%"
        )
    print(" -Cash:", cash, "EUR")
    rates = read_prices(date)
    for row in content:
        if row[2]:
            print(f" -{row[2]} ({rates[row[2]]['name']}): {row[5]:.0f} EUR")
            content_object.cryptos[row[2]] = {}
            content_object.cryptos[row[2]]["amount"] = row[3]
            content_object.cryptos[row[2]]["value"] = row[5]
    print(f"--------------------{bcolors.ENDC}")
    get_reference_content(portfolio_id, date, stats["today"], portfolio_id)
    rates = get_rates(date)
    print(f"{bcolors.WARNING}Rates {date}")
    print("")
    aux = []
    for key, value in rates.items():
        aux.append(key)
        print(
            f"{key} ({value['name']}): {value['close']} | d {value['d']}% | w {value['w']}% | m {value['m']}% | y {value['y']}% | sd {value['sd']}%"
        )
    print(f"--------------------{bcolors.ENDC}")
    return content_object


def next_period(content_object: Content):
    """Service for starting the next period"""
    coordinate_reference_actions(content_object)
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
        date_object += datetime.timedelta(1)
        if date_object > max_day_object:
            print(f"{bcolors.FAIL}No more price data available.")
            date_object -= datetime.timedelta(days)
            break

        content_object.portfolio_day = str(date_object)
        content_object.change_id += 1
        rates = read_prices(str(date_object))
        store_content(content_object, rates)

        portfolio_id = content_object.portfolio_id
        refs: dict = read_reference_portfolios(portfolio_id)
        for ref_portfolio_id in refs.values():
            content = read_portfolio_content(ref_portfolio_id)
            cash = content[0][1]
            change_id = content[0][4]
            ref_content_object = Content(
                ref_portfolio_id, content_object.portfolio_day, cash, change_id
            )
            ref_content_object.change_id += 1
            ref_content_object.cryptos = {}
            for row in content:
                crypto_id = row[2]
                crypto_amount = row[3]
                # crypto_value=row[5]
                if crypto_id:
                    if crypto_id not in ref_content_object.cryptos.keys():
                        ref_content_object.cryptos[crypto_id] = {}
                    ref_content_object.cryptos[crypto_id]["amount"] = crypto_amount
                    # ref_content_object.cryptos[crypto_id]["value"]=crypto_value
            store_content(ref_content_object, rates)


def coordinate_reference_actions(content_object: Content):
    """Coordinates actions for the reference portfolios"""
    portfolio_id = content_object.portfolio_id
    refs: dict = read_reference_portfolios(portfolio_id)

    start_date = read_portfolio_startdate(portfolio_id)
    current_date = content_object.portfolio_day

    start_date_object = datetime.datetime(
        int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10])
    ).date()

    current_date_object = datetime.datetime(
        int(current_date[0:4]), int(current_date[5:7]), int(current_date[8:10])
    ).date()

    days_passed = current_date_object - start_date_object
    days_passed = days_passed.days
    frequency = read_portfolio_frequency(content_object.portfolio_id)[0]

    if frequency == "daily":
        frequency = 1
    elif frequency == "weekly":
        frequency = 7
    elif frequency == "monthly":
        frequency = 30

    print("Refence strategies:")
    for key, ref_portfolio_id in refs.items():
        content = read_portfolio_content(ref_portfolio_id)
        cash = content[0][1]
        change_id = content[0][4]

        ref_content_object = Content(
            ref_portfolio_id, content_object.portfolio_day, cash, change_id
        )
        ref_content_object.cryptos = {}

        for row in content:
            crypto_id = row[2]
            crypto_amount = row[3]
            if crypto_id:
                if crypto_id not in ref_content_object.cryptos.keys():
                    ref_content_object.cryptos[crypto_id] = {}
                ref_content_object.cryptos[crypto_id]["amount"] = crypto_amount

        if key == "Do nothing":
            do_nothing()

        elif key == "All-in":
            all_in(ref_content_object)

        elif key == "Even":
            even(ref_content_object, days_passed, frequency)

        elif key == "Random":
            select_random(ref_content_object, days_passed, frequency)

        elif key == "Follow":
            follow_winner(ref_content_object, days_passed, frequency)

        elif key == "Contrarian":
            contrarian(ref_content_object, days_passed, frequency)


def do_nothing():
    """Keep whole portfolio in cash"""
    print('-"Do nothing" didn\'t do anything.')


def all_in(ref_content_object: Content):
    """Immediately invest everything between all the cryptos."""
    cash = ref_content_object.cash
    if cash > 1:
        investment_amount = cash / NR_OF_CRYPTOS
        for crypto_id in CRYPTO_IDS:
            buy(ref_content_object, crypto_id, investment_amount)
            print(
                f'-"All-in" invested {investment_amount:.0f} EUR in {CRYPTO_NAMES_AND_IDS[crypto_id]}.'
            )
    else:
        print('-"All-in" didn\'t do anything.')


def even(ref_content_object: Content, days_passed, frequency):
    """Splits the investment evenly between all the cryptos during a 12 month time period"""
    months = 12
    days_left = months * 30 - days_passed
    cash = ref_content_object.cash
    if days_left > 0 and cash > 0:
        total_investment = cash / (days_left / frequency)
        investment_amount = total_investment / NR_OF_CRYPTOS
        for crypto_id in CRYPTO_IDS:
            buy(ref_content_object, crypto_id, investment_amount)
            print(
                f'-"Even" invested {investment_amount:.0f} EUR in {CRYPTO_NAMES_AND_IDS[crypto_id]}.'
            )
    else:
        print('-"Even" didn\'t do anything.')


def select_random(ref_content_object: Content, days_passed, frequency):
    """Select three random cryptos each time period. Invests everything during 12 months."""
    months = 12
    select = 3

    days_left = months * 30 - days_passed
    cash = ref_content_object.cash
    if days_left > 0 and cash > 0:
        total_investment = cash / (days_left / frequency)
        investment_amount = total_investment / select

        selected_cryptos = []
        while True:
            lottery = random.choice(CRYPTO_IDS)
            if lottery not in selected_cryptos:
                selected_cryptos.append(lottery)
            if len(selected_cryptos) == select:
                break

        for crypto_id in selected_cryptos:
            buy(ref_content_object, crypto_id, investment_amount)
            print(
                f'-"Random" invested {investment_amount:.0f} EUR in {CRYPTO_NAMES_AND_IDS[crypto_id]}.'
            )

    else:
        print('-"Random" didn\'t do anything.')


def follow_winner(ref_content_object: Content, days_passed, frequency):
    """Invest in the crypto which has increased most during the last time period. Invest everything during 12 months."""
    months = 12

    days_left = months * 30 - days_passed
    cash = ref_content_object.cash
    if days_left > 0 and cash > 0:
        investment_amount = cash / (days_left / frequency)
        rates = get_rates(ref_content_object.portfolio_day)

        focus = ""
        if frequency == 1:
            focus = "d"
        elif frequency == 7:
            focus = "w"
        elif frequency == 30:
            focus = "m"
        highest_crypto = ""
        highest_change = None
        for key, value in rates.items():
            if highest_change is None:
                highest_change = value[focus]
                highest_crypto = key
            elif value[focus] > highest_change:
                highest_change = value[focus]
                highest_crypto = key

        crypto_name = rates[highest_crypto]["name"]
        buy(ref_content_object, highest_crypto, investment_amount)
        print(f'-"Follow best" invested {investment_amount:.0f} EUR in {crypto_name}.')
    else:
        print('-"Follow best" didn\'t do anything.')


def contrarian(ref_content_object: Content, days_passed, frequency):
    """Invest in the crypto which has dropped  most during the last time period. Invest everything during 12 months."""
    months = 12

    days_left = months * 30 - days_passed
    cash = ref_content_object.cash
    if days_left > 0 and cash > 0:
        investment_amount = cash / (days_left / frequency)
        rates = get_rates(ref_content_object.portfolio_day)

        focus = ""
        if frequency == 1:
            focus = "d"
        elif frequency == 7:
            focus = "w"
        elif frequency == 30:
            focus = "m"
        highest_crypto = ""
        highest_change = None
        for key, value in rates.items():
            if highest_change is None:
                highest_change = value[focus]
                highest_crypto = key
            elif value[focus] < highest_change:
                highest_change = value[focus]
                highest_crypto = key

        crypto_name = rates[highest_crypto]["name"]
        buy(ref_content_object, highest_crypto, investment_amount)
        print(f'-"Contrarian" invested {investment_amount:.0f} EUR in {crypto_name}.')
    else:
        print('-"Contrarian" didn\'t do anything.')
