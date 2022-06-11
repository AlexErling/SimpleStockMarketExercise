import logging


class Trade:
    def __init__(self, ticker, order_type, quantity, price, timestamp):
        self.ticker = ticker
        self.timestamp = timestamp
        self.quantity = quantity
        self.order_type = order_type
        self.price = price

    def __str__(self):
        return "Ticker:{} | Order Type:{} | Quantity:{} | Price:{} | Timestamp:{}".format(self.ticker, self.order_type,
                                                                                          self.quantity, self.price,
                                                                                          self.timestamp)


class TradeHistory:
    def __init__(self):
        """
        Storing the history is beyond the scope of this exercise. Would want to build a separate service to
        handle and store a high volume trades on the market
        """
        pass

    def logTrade(self, trade):
        logging.info("Trade Completed: {}".format(trade))  # Just log to terminal for now


