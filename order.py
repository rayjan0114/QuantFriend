class Order:
    def __init__(self, ordertype, stockID, buy_sell_amount, price=None):
        assert ordertype in {'MarketOrder', 'LimitOrder', 'StopLimit', 'StopLoss', 'StopLossLimit', 'MIT'}
        self.ordertype = ordertype
        self.stockID = stockID
        self.buy_sell_amount = buy_sell_amount
        self.price = price
    
    def __call__(self, price_now):
        return self.__getattribute__(self.ordertype)(price_now)
    
    def get_stockID(self):
        return self.stockID
    
    def MarketOrder(self, price_now):
        assert self.price is None
        return self.buy_sell_amount, price_now
    
    def LimitOrder(self, portfolio):
        return
    
    def StopLimit(self, portfolio):
        return

    def StopLoss(self, portfolio):
        return
    
    def StopLossLimit(self, portfolio):
        return
    
    def MIT(self, portfolio):
        return
 

if __name__ == '__main__':
    order = Order('MarketOrder', '2380', 1.0)
    price = 30
    amount, price = order(price)
    print(f"trading volume: {amount}, strike price: {price}")
