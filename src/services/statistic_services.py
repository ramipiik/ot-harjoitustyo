from sqlite3.dbapi2 import Error
import numpy as np
from repositories.price_repository import read_volatility_data
from repositories.price_repository import read_prices_for_statistics
from repositories.content_repository import read_portfolio_history, read_portfolio_content


def calculate_price_volatility(end_day):
    """Method for calculating volatility of the price"""
    rows = read_volatility_data(end_day)
    data = {}
    for row in rows:
        if row[0] not in data:
            data[row[0]] = {}
            data[row[0]]['prices'] = []
        data[row[0]]["prices"].append(row[1])
    for value in data.values():
        value['vol'] = round(
            np.std(value['prices'])/np.mean(value['prices'])*100)
        # print(f"Crypto_id {key}, vol: {value['vol']}%, price days: {len(value['prices'])}")
    return data


def get_price_statistics(date):
    """Method for calculating price statistics"""
    price_data: dict = read_prices_for_statistics(date)
    volatility_data: dict = calculate_price_volatility(date)
    rows_today = price_data["today"]
    rows_1d = price_data["1d"]
    rows_7d = price_data["7d"]
    rows_30d = price_data["30d"]
    rows_365d = price_data["365d"]

    rates = {}
    if rows_today:
        for number, row in enumerate(rows_today):
            # print("n", n)
            values = {}
            values["name"] = rows_today[number][1]
            try:
                values["close"] = rows_today[number][2]
            except Error:
                values["close"] = '--'
            try:
                values["open"] = rows_today[number][3]
            except Error:
                values["open"] = '--'
            try:
                values["high"] = rows_today[number][4]
            except Error:
                values["high"] = '--'
            try:
                values["low"] = rows_today[number][4]
            except Error:
                values["low"] = '--'
            try:
                values["1d"] = rows_1d[number][2]
            except Error:
                values["1d"] = '--'
            try:
                values["7d"] = rows_7d[number][2]
            except Error:
                values["7d"] = '--'
            try:
                values["30d"] = rows_30d[number][2]
            except Error:
                values["30d"] = '--'
            try:
                values["365d"] = rows_365d[number][2]
            except Error:
                values["365d"] = '--'
            values["vol"] = volatility_data[row[0]]['vol']
            rates[row[0]] = values

    for value in rates.values():
        if value["1d"] != '--':
            value["1d"] = round(
                100*(value["close"]-value["1d"])/value["1d"], 2)
        if value["7d"] != '--':
            value["7d"] = round(
                100*(value["close"]-value["7d"])/value["7d"], 2)
        if value["30d"] != '--':
            value["30d"] = round(
                100*(value["close"]-value["30d"])/value["30d"], 2)
        if value["365d"] != '--':
            value["365d"] = round(
                100*(value["close"]-value["365d"])/value["365d"], 2)
        # print (f"{value}")
        value["d/w"] = '--'
        value["w/m"] = '--'
        value["m/y"] = '--'
        if value["1d"] != '--' and value["7d"] != '--':
            try:
                value["d/w"] = round(value["1d"]/value["7d"], 2)
            except Error as error:
                pass
        if value["7d"] != '--' and value["30d"] != '--':
            try:
                value["w/m"] = round(value["7d"]/value["30d"], 2)
            except Error as error:
                pass
        if value["30d"] != '--' and value["365d"] != '--':
            try:
                value["m/y"] = round(value["30d"]/value["365d"], 2)
            except Error as error:
                pass
    return rates


def get_portfolio_statistics(portfolio_id):
    """Method for calculating portfolio statistics"""
    portfolio_history = read_portfolio_history(portfolio_id)[1:]
    stats = {}
    volatility='--'
    stats["vol"] = volatility
    if len(portfolio_history)>0:
        volatility = np.std(portfolio_history)/np.mean(portfolio_history)*100
        stats["vol"] = round(volatility)
    try:
        today = round(portfolio_history[-1])
    except Error:
        content= read_portfolio_content(portfolio_id)
        today = content[0][1]
    stats["today"] = today
    try:
        stats["d"] = round(
            100*(today-portfolio_history[-1-1])/portfolio_history[-1-1], 2)
    except Error:
        stats["d"] = '--'
    try:
        stats["w"] = round(
            100*(today-portfolio_history[-1-7])/portfolio_history[-1-7], 2)
    except Error:
        stats["w"] = '--'
    try:
        stats["m"] = round(
            100*(today-portfolio_history[-1-30])/portfolio_history[-1-30], 2)
    except Error:
        stats["m"] = '--'
    try:
        stats["y"] = round(
            100*(today-portfolio_history[-1-365])/portfolio_history[-1-365], 2)
    except Error:
        stats["y"] = '--'
    return stats
