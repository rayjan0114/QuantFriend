# import pandas_datareader.data as web
from datetime import datetime
from datetime import timedelta
import pandas as pd
import yfinance as yf


def get_fake_data(scale=20):
    """
    faking a very big dataset
    """
    data = yf.download("SPY",start="2015-01-01", end="2020-01-01", interval='1d',group_by="ticker")
    data2 = data.sort_values(by='Date', ascending=False)
    fake_data = [data, data2]
    for _ in range(scale):
        fake_data += fake_data
    fake_data = pd.concat(fake_data)
    start = datetime.strptime("2020-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    fake_data['Date'] = [start + i * timedelta(minutes=1) for i in range(len(fake_data))]
    # fake_data['Date'] = pd.to_datetime(fake_data['Date'], format='%Y-%m-%d %H:%M:%S')
    fake_data.set_index(fake_data['Date'], inplace=True)
    fake_data = fake_data.drop(['Date'], axis=1)
    return fake_data
    
def get_sample_data():
    data = yf.download("SPY",start="2019-01-01", end="2020-01-01", interval='1d', group_by="ticker")
    return data


if __name__ == '__main__':
    import time
    start = time.time()
    data = get_fake_data(10)
    print(f"data length: {len(data)}")
    print(f"takes {time.time() - start} s")
