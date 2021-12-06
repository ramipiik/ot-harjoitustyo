from services.statistic_services import get_price_statistics
from ui.styles import bcolors


def get_rates(date):
    """Service for fetching and printing crypto rates"""
    if date:
        rates = get_price_statistics(date)
    return rates

