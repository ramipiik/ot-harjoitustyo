from repositories.read_prices import get_prices


class Content:
    def __init__(self, portfolio_id, portfolio_day, cash, change_id):
        #initial_content=[portfolio.id, first_day, initial_capital, 1]
        self.portfolio_id=portfolio_id
        self.portfolio_day=portfolio_day
        self.cash=cash
        self.change_id=change_id
        self.cryptos={}
    
    def get_cash(self):
        return self.cash

    #CALCULATES THE EUR VALUE OF THE ITEMS IN THE PORTFOLIO ON A GIVEN DATE
    def get_portfolio(self, date):
        rates=get_prices(date)
        # print("rates", rates)
        for key, value in self.portfolio.items():
            price_of_the_day=rates[key]["close"]
            self.portfolio[key]=[self.portfolio[key][0], self.portfolio[key][0]*price_of_the_day]
        return self.portfolio
    
    def buy(self, crypto_id, amount):
        self.cash-=amount #Lisää tsekki onko tarpeeksi rahaa
        date=self.portfolio_day
        self.change_id+=1
        change_id=self.change_id
        prices=get_prices(date)
        price=prices[crypto_id]['close']
        if crypto_id in self.cryptos.keys():
            before=self.cryptos[crypto_id] 
            after=before+amount/price 
            self.cryptos[crypto_id]=after
        else:
            self.cryptos[crypto_id]=amount/price
        
        
    
    def sell(self, currency, price, amount):
        if currency in self.portfolio.keys():
            self.cash+=amount
            before=self.portfolio[currency][0] 
            after=before-amount/price 
            self.portfolio[currency]=[after, after*price] #[määrä, arvo]
        else:
            print("you cannot sell something you don't have")
