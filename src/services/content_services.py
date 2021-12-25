import datetime
import random
from repositories.content_repository import (
    read_portfolio_content,
    store_content,
    read_portfolio_startdate,
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
from ui.text_ui.styles import ERROR_MESSAGE, bcolors


CRYPTO_NAMES_AND_IDS = read_crypto_names_and_ids()
CRYPTO_IDS = []
for key in CRYPTO_NAMES_AND_IDS:
    CRYPTO_IDS.append(key)
NR_OF_CRYPTOS = len(CRYPTO_IDS)


def buy(content_object: Content, crypto_id, investment):
    """
    Service for buying a crypto

    Args:
        content_object (Content): Content object where the investment is made
        crypto_id (string): Crypto to invest in
        investment (int): Amount to invest

    If not successul returns:
        tuple: (False, Error message:str)
    """
    response = content_object.buy(crypto_id, investment)
    if tuple.__instancecheck__(response) and response[0] is False:
        return response
    if response:
        rates = read_prices(content_object.portfolio_day)
        store_content(content_object, rates)


def sell(content_object: Content, crypto_id, investment):
    """
    Service for selling a crypto

    Args:
        content_object (Content): Content object where the sales is made
        crypto_id (string): Crypto to invest in
        investment (int): Amount to invest

    If not successul returns:
        tuple: (False, Error message:str)
    """
    response = content_object.sell(crypto_id, investment)
    if tuple.__instancecheck__(response) and response[0] is False:
        return response
    if response:
        rates = read_prices(content_object.portfolio_day)
        store_content(content_object, rates)


def get_reference_content(own_portfolio_value, portfolio_id):
    """
    Service for ordering and printing reference portfolio valuations

    Args:
        own_portfolio_value (numeric): Current value of the portfolio
        portfolio_id (int): Portfolio id

    Returns:
        list: Valuation of reference strategies
    """
    references: dict = read_reference_portfolios(portfolio_id)
    collection = []
    collection.append((own_portfolio_value, "Your portfolio", portfolio_id))
    for strategy, reference_id in references.items():
        stats = get_portfolio_statistics(reference_id)
        collection.append((stats["today"], strategy, reference_id))
    collection.sort(reverse=True)
    ordered = []
    for item in collection:
        ordered.append((item[1], item[2]))
    return ordered


def get_date(portfolio_id):
    """
    Fetches the current date of the portfolio

    Args:
        portfolio_id (int)

    Returns:
        string: current date of the porfolio
    """
    content = read_portfolio_content(portfolio_id)
    date = content[0][0]
    return date


def get_content(user, portfolio_id):
    """
    Service for fetching portfolio content.

    Args:
        user (User)
        portfolio_id (int): portfolio id

    Returns:
        tuple: (date, cash, content, content_object, rates, stats, references)
    """
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
    stats = get_portfolio_statistics(portfolio_id)
    rates = read_prices(date)
    references = get_reference_content(stats["today"], portfolio_id)
    rates = get_rates(date)
    return (date, cash, content, content_object, rates, stats, references)


def next_day(content_object, date_object):
    """
    Moves portfolio content one day forward

    Args:
        content_object (Content): Content object to be moved
        date_object (Date): New date
    """
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
            if crypto_id:
                if crypto_id not in ref_content_object.cryptos.keys():
                    ref_content_object.cryptos[crypto_id] = {}
                ref_content_object.cryptos[crypto_id]["amount"] = crypto_amount
        store_content(ref_content_object, rates)


def frequency_to_number(frequency):
    """
    Helper function. Converts number to frequency text.

    Args:
        frequency (str): daily, weekly or monthly

    Returns:
        int: 1, 7 or 30
    """
    if frequency == "daily":
        return 1
    if frequency == "weekly":
        return 7
    if frequency == "monthly":
        return 30


def next_period(content_object: Content):
    """
    Service for starting the next period

    Args:
        content_object (Content)
    """
    max_day = read_max_day()[0]
    date = content_object.portfolio_day
    frequency = read_portfolio_frequency(content_object.portfolio_id)[0]
    days = frequency_to_number(frequency)
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
        next_day(content_object, date_object)


def coordinate_reference_actions(content_object: Content):
    """
    Coordinates actions for the reference portfolios

    Args:
        content_object (Content)

    Returns:
        list: actions taken by each reference portfolio
    """
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
    days = frequency_to_number(frequency)
    action_log = []
    action_log.append("Refence strategies:")
    for strategy, ref_portfolio_id in refs.items():
        action_log = implement_reference_strategy(
            strategy, ref_portfolio_id, content_object, days_passed, days, action_log
        )
    return action_log


def implement_reference_strategy(
    strategy, ref_portfolio_id, content_object, days_passed, frequency, action_log
):
    """
    Implements the reference strategy

    Args:
        strategy (str): Name of the reference strategy
        ref_portfolio_id (int): Id of the reference portfolio
        content_object (Content): Initial Content object
        days_passed (int): Nr. of days passed since the start of the portfolio
        frequency (int): Nr. of days to move forward
        action_log (list): List where actions of the reference strategies are collected

    Returns:
        [type]: [description]
    """
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
    rates = get_rates(ref_content_object.portfolio_day)
    if strategy == "Do nothing":
        action_log = do_nothing(action_log)
    elif strategy == "All-in":
        action_log = all_in(ref_content_object, action_log)
    elif strategy == "Even":
        action_log = even(ref_content_object, days_passed,
                          frequency, action_log)
    elif strategy == "Random":
        action_log = select_random(
            ref_content_object, days_passed, frequency, action_log)
    elif strategy == "Follow":
        action_log = follow_winner(
            ref_content_object, days_passed, frequency, action_log, rates
        )
    elif strategy == "Contrarian":
        action_log = contrarian(
            ref_content_object, days_passed, frequency, action_log, rates
        )
    return action_log


def do_nothing(action_log):
    """
    Keep whole portfolio in cash

    Args:
        action_log (list): List where actions of the reference strategies are collected

    Returns:
        (list): List where actions of the reference strategies are collected
    """
    action_log.append('-"Do nothing" didn\'t do anything.')
    return action_log


def all_in(ref_content_object: Content, action_log):
    """
    Immediately invest everything between all the cryptos

    Args:
        ref_content_object (Content): Content object of the reference strategy
        action_log (list): List where actions of the reference strategies are collected

    Returns:
        (list): List where actions of the reference strategies are collected
    """
    cash = ref_content_object.cash
    if cash > 1:
        investment_amount = cash / NR_OF_CRYPTOS
        for crypto_id in CRYPTO_IDS:
            buy(ref_content_object, crypto_id, investment_amount)
            action_log.append(
                f'-"All-in" invested {investment_amount:.0f} EUR in {CRYPTO_NAMES_AND_IDS[crypto_id]}.'
            )
    else:
        action_log.append('-"All-in" didn\'t do anything.')
    return action_log


def even(ref_content_object: Content, days_passed, frequency, action_log):
    """
    Splits the investment evenly between all the cryptos during a 12 month time period

    Args:
        ref_content_object (Content): Content object of the reference strategy
        days_passed (int): Nr. of days passed since the start of the portfolio
        frequency (int): Nr. of days to move forward
        action_log (list): List where actions of the reference strategies are collected

    Returns:
        (list): List where actions of the reference strategies are collected
    """
    months = 12
    days_left = months * 30 - days_passed
    cash = ref_content_object.cash
    if days_left > 0 and cash > 0:
        total_investment = cash / (days_left / frequency)
        investment_amount = total_investment / NR_OF_CRYPTOS
        for crypto_id in CRYPTO_IDS:
            buy(ref_content_object, crypto_id, investment_amount)
            action_log.append(
                f'-"Even" invested {investment_amount:.0f} EUR in {CRYPTO_NAMES_AND_IDS[crypto_id]}.'
            )
    else:
        action_log.append('-"Even" didn\'t do anything.')
    return action_log


def select_random(ref_content_object: Content, days_passed, frequency, action_log):
    """
    Select three random cryptos each time period. Invests everything during 12 months.

    Args:
        ref_content_object (Content): Content object of the reference strategy
        days_passed (int): Nr. of days passed since the start of the portfolio
        frequency (int): Nr. of days to move forward
        action_log (list): List where actions of the reference strategies are collected

    Returns:
        (list): List where actions of the reference strategies are collected
    """
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
            action_log.append(
                f'-"Random" invested {investment_amount:.0f} EUR in {CRYPTO_NAMES_AND_IDS[crypto_id]}.'
            )
    else:
        action_log.append('-"Random" didn\'t do anything.')
    return action_log


def frequency_to_focus(frequency):
    """
    Helper function. Converts frequency number to letter d(aily), w(weekly) or m(onthly)

    Args:
        frequency (int): 1, 7 or 30

    Returns:
        string: 'd', 'w' or 'm'
    """
    if frequency == 1:
        return "d"
    if frequency == 7:
        return "w"
    if frequency == 30:
        return "m"


def follow_winner(
    ref_content_object: Content, days_passed, frequency, action_log, rates
):
    """
    Invest in the crypto which has increased most. Invests everything during 12 months.

    Args:
        ref_content_object (Content): Content object of the reference strategy
        days_passed (int): Nr. of days passed since the start of the portfolio
        frequency (int): Nr. of days to move forward
        action_log (list): List where actions of the reference strategies are collected
        rates (dict): Crypto rates

    Returns:
        (list): List where actions of the reference strategies are collected
    """

    months = 12
    days_left = months * 30 - days_passed
    cash = ref_content_object.cash
    if days_left > 0 and cash > 0:
        investment_amount = cash / (days_left / frequency)
        focus = frequency_to_focus(frequency)
        highest_crypto = ""
        highest_change = None
        for crypto, value in rates.items():
            if highest_change is None:
                highest_change = value[focus]
                highest_crypto = crypto
            elif value[focus] > highest_change:
                highest_change = value[focus]
                highest_crypto = crypto
        crypto_name = rates[highest_crypto]["name"]
        buy(ref_content_object, highest_crypto, investment_amount)
        action_log.append(
            (f'-"Follow best" invested {investment_amount:.0f} EUR in {crypto_name}.')
        )
    else:
        action_log.append('-"Follow best" didn\'t do anything.')
    return action_log


def contrarian(ref_content_object: Content, days_passed, frequency, action_log, rates):
    """
    Invest in the crypto which has dropped most. Invests everything during 12 months.

    Args:
        ref_content_object (Content): Content object of the reference strategy
        days_passed (int): Nr. of days passed since the start of the portfolio
        frequency (int): Nr. of days to move forward
        action_log (list): List where actions of the reference strategies are collected
        rates (dict): Crypto rates

    Returns:
        (list): List where actions of the reference strategies are collected
    """
    months = 12
    days_left = months * 30 - days_passed
    cash = ref_content_object.cash
    if days_left > 0 and cash > 0:
        investment_amount = cash / (days_left / frequency)
        focus = frequency_to_focus(frequency)
        highest_crypto = ""
        highest_change = None
        for crypto, value in rates.items():
            if highest_change is None:
                highest_change = value[focus]
                highest_crypto = crypto
            elif value[focus] < highest_change:
                highest_change = value[focus]
                highest_crypto = crypto
        crypto_name = rates[highest_crypto]["name"]
        buy(ref_content_object, highest_crypto, investment_amount)
        action_log.append(
            f'-"Contrarian" invested {investment_amount:.0f} EUR in {crypto_name}.'
        )
    else:
        action_log.append('-"Contrarian" didn\'t do anything.')
    return action_log
