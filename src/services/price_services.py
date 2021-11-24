from repositories.price_repository import read_prices
from services.statistic_services import get_price_statistics
from ui.styles import bcolors


def get_rates(date):
    """Service for fetching and printing crypto rates"""
    # To do: Move prints to text-ui?
    print(f"{bcolors.WARNING}Rates {date}")
    print("")
    if date:
        rates = get_price_statistics(date)
        aux = []
        for key, value in rates.items():
            aux.append(key)
            print(f"{key} ({value['name']}): {value['close']} | d {value['1d']}% | w {value['7d']}% | m {value['30d']}% | y {value['365d']}% | sd {value['vol']}%")
    print(f"--------------------{bcolors.ENDC}")
