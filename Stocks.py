from collections import deque
from datetime import datetime, timedelta
import pandas
import numpy as np
import Stock


class Stocks:
    def __init__(self):
        self.stock_data = {}
        self.stock_pricing = {}

    def __iter__(self):
        return iter(self.stock_pricing)

    def loadStockData(self, stock_list):
        stock_factory = Stock.StockFactory()
        for ticker, stock_type, last_dividend, fixed_dividend, par_value in stock_list:
            self.stock_data[ticker] = stock_factory.createStock(ticker, stock_type, par_value, last_dividend,
                                                                fixed_dividend)
            self.stock_pricing[ticker] = StockPricing(ticker)

    def loadStockDataFromCSV(self, csv_path):
        stock_data = pandas.read_csv(csv_path)
        stock_data = stock_data.replace({np.nan: None})
        stock_list = stock_data.values.tolist()

        return self.loadStockData(stock_list)

    def updateStockPricing(self, trade):

        ticker = trade.ticker

        if ticker not in self.stock_data.keys():
            return -1

        else:
            ticker_pricing = self.stock_pricing[ticker]
            ticker_pricing.addToPriceQueue(trade)
            return 0

    def getStockVWAP(self, ticker):
        if ticker not in self.stock_data.keys():
            return -1

        return self.stock_pricing[ticker].getVWAP()

    def getStockDividendYield(self, ticker, price):
        if ticker not in self.stock_data.keys():
            return -1

        return self.stock_data[ticker].getDividendYield(price)

    def getStockPER(self, ticker, price):
        if ticker not in self.stock_data.keys():
            return -1

        return self.stock_data[ticker].getPER(price)


class StockPricing:

    def __init__(self, ticker):
        self.ticker = ticker
        self.vwap_5_min = float("nan")
        self.lastUpdate = datetime.now() - timedelta(seconds=1)
        self.pre_queue = deque()  # To process new values
        self.queue = deque()  # Storing values for current vwap_5_min
        self.cumulative_quantity = 0
        self.cumulative_price_volume = 0

    def addToPriceQueue(self, trade):
        self.pre_queue.append((trade.timestamp, float(trade.quantity), float(trade.price)))

    def getVWAP(self):

        # Can throttle how often it updates -> would probably want this price updates to be handled by separate
        # worker threads
        if self.lastUpdate < datetime.now() - timedelta(seconds=1):
            self.updateVWAP()

        return self.vwap_5_min

    def updateVWAP(self):
        timestamp_start = datetime.now() - timedelta(minutes=5)
        while self.queue and self.queue[0][0] < timestamp_start:

            _, quantity, price = self.queue.popleft()
            self.cumulative_price_volume -= quantity * price
            self.cumulative_quantity -= quantity

        while self.pre_queue:

            timestamp, quantity, price = self.pre_queue.popleft()
            self.cumulative_price_volume += quantity * price
            self.cumulative_quantity += quantity
            self.queue.append((timestamp, quantity, price))

        if self.cumulative_quantity == 0:
            self.vwap_5_min = float("nan")
        else:
            self.vwap_5_min = float(self.cumulative_price_volume / self.cumulative_quantity)



        self.lastUpdate = datetime.now()
