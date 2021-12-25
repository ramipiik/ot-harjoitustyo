from services.statistic_services import get_price_statistics


def get_rates(date):
    """
    Service for fetching and printing crypto rates

    Args:
        date (string): date from which to read prices

    Returns:
        list: price statistics
    """
    if date:
        rates = get_price_statistics(date)
    return rates
