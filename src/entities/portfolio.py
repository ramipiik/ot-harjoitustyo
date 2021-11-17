from repositories.read_prices import get_prices


class Portfolio:
    def __init__(self, user_id, name, frequency, periods=None):
        self.frequency=frequency
        self.user_id=user_id
        self.name=name
        self.periods=periods
        self.id=None #created in the database
    
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
    
    def buy(self, currency, price, investment):
        self.cash-=investment
        if currency in self.portfolio.keys():
            before=self.portfolio[currency][0] 
            after=before+investment/price 
            self.portfolio[currency]=[after, after*price] #[määrä, arvo]
        else:
            self.portfolio[currency]=[investment/price, price]
    
    def sell(self, currency, price, amount):
        if currency in self.portfolio.keys():
            self.cash+=amount
            before=self.portfolio[currency][0] 
            after=before-amount/price 
            self.portfolio[currency]=[after, after*price] #[määrä, arvo]
        else:
            print("you cannot sell something you don't have")
