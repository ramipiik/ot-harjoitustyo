from repositories.price_repository import read_prices
from ui.styles import bcolors


def get_rates(date):
    """Service for fetching and printing crypto rates"""
    # To do: Move prints to text-ui?
    print(f"{bcolors.WARNING}Rates {date}")
    print("")
    if date:
        rates = read_prices(date)
        aux = []
        for key, value in rates.items():
            aux.append(key)
            print(f"{key} ({value['name']}): {value['close']:.4f}")
    print(f"--------------------{bcolors.ENDC}")
