import pandas as pd
import time
import numpy as np

class BackTest:
    def __init__(self, trading_data, indexes):
        """
        trading_data: time series data which include the target you want to trade
        indexes: the supportive data which might help yout trader work better
        """
        assert len(trading_data) == len(indexes)
        self.trading_data = trading_data
        self.indexes = indexes
        self.commission = 0.01
        result_length = len(self) + 1  # dummy starting point [ 0, ...
        self.result = {
            'account': np.zeros(result_length),
            'unrealized_account': np.zeros(result_length),
            'signal':{}  # Dict[stockID, buy sell amount]
        }
        self.portfolio = {}
        self.count = 0
        
    def __len__(self):
        return len(self.trading_data)
    
    def renew_unrealized_gains(self):
        delta_account = 0.
        for stockID, obj in self.portfolio.items():
            price_now = self.trading_data[stockID][self.count]
            delta_account += (price_now - obj['price']) * obj['amount']
        self.result['unrealized_account'][self.count] += delta_account
            
    def realize_gain(self, stockID):
        """
        Closing position to refect account
        """
        price_now = self.trading_data[stockID][self.count]
        amount = self.portfolio[stockID]['amount']
        price = self.portfolio[stockID]['price']
        self.result['account'][self.count:] += (
            price_now - price) * amount - self.cal_commisions(amount, price)
        del self.portfolio[stockID]
        
    def _append_signal_to_result(self, stockID, amount):
        if stockID in self.result['signal'] and amount != 0:
            self.result['signal'][stockID] = self.result['signal'][stockID].append(
                pd.DataFrame([amount], index=[
                    self.trading_data.index[self.count]], columns=[stockID]))
        else:
            self.result['signal'][stockID] = pd.DataFrame(
                [amount], index=[self.trading_data.index[self.count]], columns=[stockID]) 
            
    def _change_portfolio(self, stockID, price, amount):
        amount_old = self.portfolio[stockID]['amount'] if stockID in self.portfolio else 0
        price_old = self.portfolio[stockID]['price'] if stockID in self.portfolio else 0
        if amount_old + amount == 0.:
            self.realize_gain(stockID)
        else:
            total_amount = amount + amount_old
            avg_price = (price * amount + price_old * amount_old) / total_amount
            self.portfolio[stockID] = {
                'amount': total_amount,
                'price': avg_price,
            }
            self.portfolio[stockID]['amount'] = amount + amount_old
            self.portfolio[stockID]['price'] = avg_price
        
    def apply_orders_on_portfolio(self, order_list):
        for order in order_list:
            # broker收單(股票代號、買賣價、單類型)
            stockID = order.get_stockID()
            price = self.trading_data[stockID][self.count]
            
            # 搓合，決定是否成交
            amount, price = order(price)
            
            # 儲存買賣訊號
            self._append_signal_to_result(stockID, amount)
            
            # 資產扣除手續費
            self.result['account'][self.count] -= self.cal_commisions(amount, price)
            
            # 改變portfolio(持有部位清單)
            self._change_portfolio(stockID, price, amount)

    
    def evaluate(self, trader): 
        """
        Play the data tape so that the trader can do its job
        Once finished, you can access the result by get_account, or get_signals
        """
        for count in range(1, len(self)):
            self.count = count 
            t_data, i_data = self.trading_data.iloc[count], self.indexes.iloc[count]
            # trader 產生價單陣列
            order_list = trader.trade(t_data, i_data)
            
            # 將價單丟給broker決定是否成交，帳戶跟持有部位跟著改變
            self.apply_orders_on_portfolio(order_list)
            
            # 將未實現損益反映在賬戶上
            self.renew_unrealized_gains()
            
    def cal_commisions(self, amount, price):
        return self.commission * amount * price
    
    def get_account(self):
        # exclude dummy starting point [ 0, ...
        account = self.result['account'][1:] + self.result['unrealized_account'][1:]
        account = pd.DataFrame(account, columns=['account'])
        account.index = pd.to_datetime(self.trading_data.index)
        return account[:self.count]
    
    def get_signals(self):
        return self.result['signal']
    

if __name__ == '__main__':
    from mytrader import HelloWorldTrade
    from dataload import get_sample_data
    df = get_sample_data()
    trading_data = df[['Close']].rename(columns={'Close': '2380_close'})
    indexes = df  # we don't use any index to support the strategy in this hello-world trader
    start = time.time()
    back_tester = BackTest(trading_data, indexes)
    trader = HelloWorldTrade()
    back_tester.evaluate(trader)
    print((time.time() - start))
