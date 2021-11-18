from repositories.price_repository import read_prices


'''Service for fetching and printing crypto rates'''
def get_rates(date):    
    #To do: Move prints to text-ui?
    print(f"Rates {date}")
    print("")
    if date:
        rates=read_prices(date)
        aux=[]
        for key, value in rates.items():
            aux.append(key)
            print(f"{key} ({value['name']}): {value['close']:.4f}")
    print("-------------")

