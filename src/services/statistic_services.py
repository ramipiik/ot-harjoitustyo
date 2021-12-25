import numpy as np
from repositories.price_repository import read_volatility_data
from repositories.price_repository import read_prices_for_statistics
from repositories.content_repository import (
    read_portfolio_history,
    read_portfolio_content,
)


def calculate_price_volatility(end_day):
    """
    Method for calculating volatility of the price

    Args:
        end_day (string): Last day of the period

    Returns:
        list: prices volatility
    """
    rows = read_volatility_data(end_day)
    data = {}
    for row in rows:
        if row[0] not in data:
            data[row[0]] = {}
            data[row[0]]["prices"] = []
        data[row[0]]["prices"].append(row[1])
    for value in data.values():
        value["sd"] = round(np.std(value["prices"]) /
                            np.mean(value["prices"]) * 100)
    return data


def get_price_statistics(date):
    """
    Method for calculating price statistics

    Args:
        date (string): date from which to read prices

    Returns:
        list: price statistics
    """
    price_data: dict = read_prices_for_statistics(date)
    volatility_data: dict = calculate_price_volatility(date)
    rows_today = price_data["today"]
    rows_d = price_data["d"]
    rows_w = price_data["w"]
    rows_m = price_data["m"]
    rows_y = price_data["y"]
    rates = {}
    rates = organize_base_rates(
        rates, rows_today, rows_d, rows_w, rows_m, rows_y, volatility_data
    )
    rates = calculate_relations(rates)
    return rates


def organize_base_rates(
    rates, rows_today, rows_d, rows_w, rows_m, rows_y, volatility_data
):
    """Internal helper function for organizing base rates."""
    if rows_today:
        for number, row in enumerate(rows_today):
            values = {}
            values["name"] = rows_today[number][1]
            try:
                values["close"] = rows_today[number][2]
            except:
                values["close"] = "--"
            try:
                values["open"] = rows_today[number][3]
            except:
                values["open"] = "--"
            try:
                values["high"] = rows_today[number][4]
            except:
                values["high"] = "--"
            try:
                values["low"] = rows_today[number][4]
            except:
                values["low"] = "--"
            try:
                values["d"] = rows_d[number][2]
            except:
                values["d"] = "--"
            try:
                values["w"] = rows_w[number][2]
            except:
                values["w"] = "--"
            try:
                values["m"] = rows_m[number][2]
            except:
                values["m"] = "--"
            try:
                values["y"] = rows_y[number][2]
            except:
                values["y"] = "--"

            values["sd"] = volatility_data[row[0]]["sd"]
            rates[row[0]] = values
    return rates


def calculate_relations(rates):
    """
    Calculates the daily, weekly, monthly and yearly changes

    Args:
        rates (list): crypto rates

    Returns:
        list: rates with statistics
    """
    for value in rates.values():
        if value["d"] != "--":
            value["d"] = round(
                100 * (value["close"] - value["d"]) / value["d"], 2)
        if value["w"] != "--":
            value["w"] = round(
                100 * (value["close"] - value["w"]) / value["w"], 2)
        if value["m"] != "--":
            value["m"] = round(
                100 * (value["close"] - value["m"]) / value["m"], 2)
        if value["y"] != "--":
            value["y"] = round(
                100 * (value["close"] - value["y"]) / value["y"], 2)
        value["d/w"] = "--"
        value["w/m"] = "--"
        value["m/y"] = "--"
        if value["d"] != "--" and value["w"] != "--":
            try:
                value["d/w"] = round(value["d"] / value["w"], 2)
            except:
                pass
        if value["w"] != "--" and value["m"] != "--":
            try:
                value["w/m"] = round(value["w"] / value["m"], 2)
            except:
                pass
        if value["m"] != "--" and value["y"] != "--":
            try:
                value["m/y"] = round(value["m"] / value["y"], 2)
            except:
                pass
    return rates


def get_portfolio_statistics(portfolio_id):
    """
    Method for calculating portfolio statistics

    Args:
        portfolio_id (int)

    Returns:
        list: statistics of the given portfolio
    """
    data = read_portfolio_history(portfolio_id)
    values: dict = data[1]
    min_date = data[0]
    start_value = values[min_date]
    stats = {}
    volatility = "--"
    stats["sd"] = volatility
    portfolio_history = []
    for value in values.values():
        portfolio_history.append(value)
    if len(portfolio_history) > 0:
        volatility = np.std(portfolio_history) / \
            np.mean(portfolio_history) * 100
        stats["sd"] = round(volatility)
        today = round(portfolio_history[-1])
    else:
        content = read_portfolio_content(portfolio_id)
        today = content[0][1]
    stats["today"] = today
    stats["all-time"] = int(round((today - start_value) /
                            start_value * 100, 0))
    try:
        stats["d"] = round(
            100 * (today - portfolio_history[-1 - 1]
                   ) / portfolio_history[-1 - 1], 2
        )
    except:
        stats["d"] = "--"
    try:
        stats["w"] = round(
            100 * (today - portfolio_history[-1 - 7]
                   ) / portfolio_history[-1 - 7], 1
        )
    except:
        stats["w"] = "--"
    try:
        stats["m"] = int(
            round(
                100 *
                (today - portfolio_history[-1 - 30]
                 ) / portfolio_history[-1 - 30],
                0,
            )
        )
    except:
        stats["m"] = "--"
    try:
        stats["y"] = int(
            round(
                100
                * (today - portfolio_history[-1 - 365])
                / portfolio_history[-1 - 365],
                0,
            )
        )
    except:
        stats["y"] = "--"
    return stats


def calculate_portfolio_relations(stats, today, start_value, portfolio_history):
    """
    Method for calculating value development of the portfolio

    Args:
        stats (list): statistics of portfolio
        today (Date): current date
        start_value (int): initial capital
        portfolio_history (list): value history of the portfolio

    Returns:
        list: daily, weekly, monthly and yearly value development
    """
    stats["all-time"] = int(round((today - start_value) /
                            start_value * 100, 0))
    try:
        stats["d"] = round(
            100 * (today - portfolio_history[-1 - 1]
                   ) / portfolio_history[-1 - 1], 2
        )
    except:
        stats["d"] = "--"
    try:
        stats["w"] = round(
            100 * (today - portfolio_history[-1 - 7]
                   ) / portfolio_history[-1 - 7], 1
        )
    except:
        stats["w"] = "--"
    try:
        stats["m"] = int(
            round(
                100 *
                (today - portfolio_history[-1 - 30]
                 ) / portfolio_history[-1 - 30],
                0,
            )
        )
    except:
        stats["m"] = "--"
    try:
        stats["y"] = int(
            round(
                100
                * (today - portfolio_history[-1 - 365])
                / portfolio_history[-1 - 365],
                0,
            )
        )
    except:
        stats["y"] = "--"
    return stats
