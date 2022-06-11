from enum import Enum
from abc import abstractmethod


class Stock:
    def __init__(self, ticker, stock_type, par_value, last_dividend):
        self.ticker = ticker
        self.stock_type = stock_type
        self.par_value = par_value
        self.last_dividend = last_dividend

    def getPER(self, price):
        if self.last_dividend == 0:
            return float('nan')

        return float(price / self.last_dividend)

    @abstractmethod
    def getDividendYield(self, price):
        pass


class CommonStock(Stock):
    def __init__(self, ticker, stock_type, par_value, last_dividend):
        Stock.__init__(self, ticker, stock_type, par_value, last_dividend)

    def getDividendYield(self, price):
        if price == 0:
            return float('nan')

        return float(self.last_dividend / price)


class PreferredStock(Stock):
    def __init__(self, ticker, stock_type, par_value, last_dividend, fixed_dividend):
        Stock.__init__(self, ticker, stock_type, par_value, last_dividend)
        self.fixed_dividend = fixed_dividend

    def getDividendYield(self, price):
        if price == 0:
            return float('nan')

        return float((self.fixed_dividend + self.par_value) // price)


class StockEnum(Enum):
    Common = 0
    Preferred = 1


class StockFactory:
    def createStock(self, ticker, stock_type, par_value, last_dividend, fixed_dividend):

        stock_enum = StockEnum[stock_type]

        if stock_enum == StockEnum.Common:
            return CommonStock(ticker, stock_type, par_value, last_dividend)

        elif stock_enum == StockEnum.Preferred:
            if fixed_dividend is None:
                raise ValueError("Need a valid fixed dividend for preferred stock")

            return PreferredStock(ticker, stock_type, par_value, last_dividend, fixed_dividend)

        else:
            raise ValueError("Invalid Stock Type")
