from repositories.price_repository import read_prices

'''Class for managing portfolio content'''
class Content:
    def __init__(self, portfolio_id, portfolio_day, cash, change_id):
        self.portfolio_id=portfolio_id
        self.portfolio_day=portfolio_day
        self.cash=cash
        self.change_id=change_id
        self.cryptos={}
    
    '''Method for buying a crypto'''
    def buy(self, crypto_id, investment):
        if investment>self.cash:
            print("Not enough cash")
            return
        self.cash-=investment
        date=self.portfolio_day
        self.change_id+=1
        prices=read_prices(date)
        price=prices[crypto_id]['close']
        if crypto_id in self.cryptos.keys():
            before=self.cryptos[crypto_id]["amount"] 
            after=before+investment/price 
            self.cryptos[crypto_id]["amount"]=after
            self.cryptos[crypto_id]["value"]=after*price
        else:
            self.cryptos[crypto_id]={}
            self.cryptos[crypto_id]["amount"]=investment/price
            self.cryptos[crypto_id]["value"]=investment
        
    '''Method for buying a crypto. Allows short selling.'''    
    def sell(self, crypto_id, investment):
        self.cash+=investment
        date=self.portfolio_day
        self.change_id+=1
        prices=read_prices(date)
        price=prices[crypto_id]['close']
        if crypto_id in self.cryptos.keys():
            before=self.cryptos[crypto_id]["amount"] 
            after=before-investment/price 
            self.cryptos[crypto_id]["amount"]=after
            self.cryptos[crypto_id]["value"]=after*price
        else:
            self.cryptos[crypto_id]={}
            self.cryptos[crypto_id]["amount"]=-investment/price
            self.cryptos[crypto_id]["value"]=-investment
