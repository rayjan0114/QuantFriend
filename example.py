if __name__ == '__main__':
    from talib import SMA
    import pandas as pd
    from dataload import get_sample_data
    from mytrader import HelloWorldTrade
    from backtest import BackTest
    from utils.visualize import visuialize_performance
    df = get_sample_data()
    trading_data = df[['Close']].rename(columns={'Close': '2380_close'})
    indexes = df  # we don't use any index to support the strategy in this hello-world trader
    trader = HelloWorldTrade()
    back_tester = BackTest(trading_data, indexes)
    back_tester.evaluate(trader)
    data_to_plot = trading_data.copy()
    data_to_plot['13MA'] = SMA(trading_data['2380_close'], 13)
    data_to_plot['34MA'] = SMA(trading_data['2380_close'], 34)
    visuialize_performance(
        back_tester, 
        data_to_plot[['2380_close']],
        data_to_plot[['13MA']],
        data_to_plot[['34MA']])
    print("see result in output dir!")
