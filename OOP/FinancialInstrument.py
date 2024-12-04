import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class FinancialInstrumentBase():
    ''' Class to analyze finiancial instruments like stocks

        Atributes
        =========
        tickers: str
            ticker symbol with which to work with
        start: str
            start date of the retrieval
        end: str
            end date for the retrieval
    '''
    def __init__(self, ticker, start, end):
        if ticker is not None:
            self._ticker = ticker  
            self.start = start
            self.end = end
            self.get_data()
            self.log_returns()

    def __repr__(self):
        return "FiniancialInstrument(ticker = {}, start = {}, end = {})".format(self._ticker,
                                                                                self.start, self.end)

    def get_data(self):
        raw = yf.download(self._ticker, self.start, self.end).Close.to_frame()
        raw.rename(columns = {"Close":"price"}, inplace = True)
        self.data = raw

    def log_returns(self):
        self.data["log_returns"] = np.log(self.data.price / self.data.price.shift(1))
        return self.data["log_returns"]

    def plot_prices(self):
        self.data.price.plot(figsize=(12, 8))
        # plt.title("Price Chart:{}".format(self._ticker), fontsize = 15)

    def plot_returns(self, kind="ts"):
        ''' plots log returns either as a time series ("ts") or as a histogram ("hist")
        '''
        if kind == "ts":
            self.data['log_returns'].plot(figsize=(12, 8))
        elif kind == "hist":
            self.data['log_returns'].hist(figsize=(12, 8), bins=int(np.sqrt(len(self.data))))

    def set_ticker(self, ticker=None):
        if ticker is not None:
            self._ticker = ticker  # Update the private _ticker attribute
            self.get_data()  # Fetch new data for the new ticker
            self.log_returns()  # Recompute log returns for the new data

    def mean_return(self, freq = None):
        if freq is None:
            return self.data.log_returns.mean()
        else:
            resample_price = self.data.price.resample(freq).last()
            resample_returns = np.log(resampled_price / resample_price.shift(1))
            return resample_returns.mean()

    def std_returns(self, freq = None):
        if freq is None:
            return self.data.log_returns.std()
        else:
            resampled_price = self.data.price.resample(freq).last()
            resampled_returns = np.log(resampled_price / resampled_price.shift(1))
            return resampled_returns.std()

    def annualized_perf(self):
        mean_return = round(self.data.log_returns.mean() * 252, 3)
        risk = round(self.data.log_returns.std() * np.sqrt(252), 3)
        print("Return: {} | Risk: {}".format(mean_return, risk))