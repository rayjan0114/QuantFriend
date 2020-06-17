import numpy as np
from talib import SMA
from order import Order



class HelloWorldTrade:
    def __init__(self):
        self.close = np.array([])
        
    def trade(self, trading_data, indexes=None):
        self.close = np.concatenate([self.close, np.asarray([trading_data['2380_close']])])
        order_list = []
        if len(self.close) > 35:
            sma13_old, sma13 = SMA(self.close[-14:], 13)[-2:]
            sma34_old, sma34 = SMA(self.close[-35:], 34)[-2:]
            if sma13 - sma34 > 0 and sma13_old - sma34_old < 0:
                order_list.append(Order('MarketOrder', '2380_close', 1.0))
            elif sma13 - sma34 < 0 and sma13_old - sma34_old > 0:
                order_list.append(Order('MarketOrder', '2380_close', -1.0))
        
        return order_list
    

if __name__ == '__main__':
    trader = HelloWorldTrade()
    