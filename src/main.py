from ui.text_ui import start
from repositories.price_repository import calculate_volatility
from services.portfolio_services import FIRST_DAY
import numpy as np
from statistics import mean



# data=calculate_volatility(FIRST_DAY)
# for key, value in data.items():
#     data[key]['vol'] = round(np.std(value['prices'])/np.mean(value['prices'])*100)
#     print(f"Crypto_id {key}, vol: {value['vol']}%, price days: {len(value['prices'])}")
# exit()

start()
