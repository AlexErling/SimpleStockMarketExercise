from datetime import datetime
import random
import time
import logging
import Stocks
import Trades

class StockMarket:
    def __init__(self, name):
        self.name = name
        self.stocks = Stocks.Stocks()
        self.trade_history = Trades.TradeHistory()

    def addTrade(self, ticker, order_type, quantity, price):
        if quantity == 0 or price == 0:
            return -1
        else:
            trade = Trades.Trade(ticker, order_type, quantity, price, datetime.now())
            result = self.stocks.updateStockPricing(trade)  # Send to pricing system
            self.trade_history.logTrade(trade)  # Send to logging system

        return result

    def calcIndex(self):
        nth_root = 0
        total_product = 1

        for stock in self.stocks:
            nth_root += 1
            total_product *= self.stocks.getStockVWAP(stock)

        return total_product ** (1 / nth_root)

