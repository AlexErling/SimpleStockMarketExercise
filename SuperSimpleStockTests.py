import unittest
import fastapi
import Stock
import StockMarket
import Trades
import time
import datetime
import math
from fastapi.testclient import TestClient
from main import APIRoutes


class TestStockMethods(unittest.TestCase):

    def setUp(self):
        self.market = StockMarket.StockMarket("Test")

        stock_list = [['TEA', 'Common', 0, None, 100], ['POP', 'Common', 8, None, 100], ['ALE', 'Common', 23, None, 60],
                      ['GIN', 'Preferred', 8, 0.02, 100], ['JOE', 'Common', 13, None, 250]]

        self.market.stocks.loadStockData(stock_list)

        for i in range(10):
            self.market.addTrade("TEA", "Buy", 100, 50)
            self.market.addTrade("POP", "Buy", 90, 40)
            self.market.addTrade("ALE", "Buy", 80, 30)
            self.market.addTrade("GIN", "Buy", 70, 20)
            self.market.addTrade("JOE", "Buy", 60, 10)
            self.market.addTrade("TEA", "Sell", 50, 10)
            self.market.addTrade("POP", "Sell", 40, 20)
            self.market.addTrade("ALE", "Sell", 30, 30)
            self.market.addTrade("GIN", "Sell", 20, 40)
            self.market.addTrade("JOE", "Sell", 300, 50)

    def testCommonStock(self):
        stock = Stock.CommonStock("TEA", 0, 100, 50)
        self.assertEqual(stock.ticker, "TEA")
        self.assertEqual(0, stock.stock_type)
        self.assertEqual(stock.par_value, 100)
        self.assertEqual(stock.last_dividend, 50)

    def testPreferredStock(self):
        stock = Stock.PreferredStock("TEA", 0, 100, 50, 100)
        self.assertEqual(stock.ticker, "TEA")
        self.assertEqual(0, stock.stock_type)
        self.assertEqual(stock.last_dividend, 50)
        self.assertEqual(stock.par_value, 100)

    def testTradeUpdatesData(self):
        vwap_1 = self.market.stocks.getStockVWAP("TEA")
        self.assertAlmostEqual(36.67, round(vwap_1, 2))
        result = self.market.addTrade("TEA", "Buy", 1000, 500)
        time.sleep(1)
        self.assertEqual(result, 0)
        vwap_1 = self.market.stocks.getStockVWAP("TEA")
        self.assertAlmostEqual(222.00, round(vwap_1, 2))

        result = self.market.addTrade("BAD", "Buy", 1000, 500)
        self.assertEqual(result, -1)
        pass

    def testVWAP(self):
        vwap_1 = self.market.stocks.getStockVWAP("TEA")
        vwap_2 = self.market.stocks.getStockVWAP("POP")
        vwap_3 = self.market.stocks.getStockVWAP("ALE")
        vwap_4 = self.market.stocks.getStockVWAP("GIN")
        vwap_5 = self.market.stocks.getStockVWAP("JOE")

        self.assertAlmostEqual(36.67, round(vwap_1, 2))
        self.assertAlmostEqual(33.85, round(vwap_2, 2))
        self.assertAlmostEqual(30.00, round(vwap_3, 2))
        self.assertAlmostEqual(24.44, round(vwap_4, 2))
        self.assertAlmostEqual(43.33, round(vwap_5, 2))

    def testPER(self):
        per_1 = self.market.stocks.getStockPER("TEA", 20)
        per_2 = self.market.stocks.getStockPER("POP", 20)
        per_3 = self.market.stocks.getStockPER("ALE", 20)
        per_4 = self.market.stocks.getStockPER("GIN", 20)
        per_5 = self.market.stocks.getStockPER("JOE", 20)
        per_6 = self.market.stocks.getStockPER("BAD", 20)

        self.assertTrue(math.isnan(per_1))
        self.assertAlmostEqual(2.5, round(per_2, 2))
        self.assertAlmostEqual(.87, round(per_3, 2))
        self.assertAlmostEqual(2.5, round(per_4, 2))
        self.assertAlmostEqual(1.54, round(per_5, 2))
        self.assertEqual(per_6, -1)

    def testDividend(self):
        # Common
        div_1 = self.market.stocks.getStockDividendYield("POP", 10)

        # Preferred
        div_2 = self.market.stocks.getStockDividendYield("GIN", 20)

        # BAD Ticker
        div_3 = self.market.stocks.getStockDividendYield("BAD", 20)

        self.assertEqual(.8, div_1)
        self.assertEqual(5, div_2)
        self.assertEqual(div_3, -1)

    def testGetIndex(self):
        index = self.market.calcIndex()
        self.assertAlmostEqual(33.05, round(index, 2))

    def testStockFactory(self):
        sf = Stock.StockFactory()
        stock_one = sf.createStock("ABC", "Common", 100, 10, None)

        stock_two = sf.createStock("ABC", "Preferred", 100, 3, 20)

        self.assertIsInstance(stock_one, Stock.CommonStock)
        self.assertIsInstance(stock_two, Stock.PreferredStock)

    def testTrade(self):
        timestamp = datetime.datetime.now()
        trade = Trades.Trade("ABC", "Buy", 100, 40, timestamp)

        self.assertEqual(trade.price, 40)
        self.assertEqual(trade.ticker, "ABC")
        self.assertEqual(trade.quantity, 100)
        self.assertEqual(trade.order_type, "Buy")
        self.assertEqual(trade.timestamp, timestamp)


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = fastapi.FastAPI()
        self.market = StockMarket.StockMarket("Test")

        stock_list = [['TEA', 'Common', 0, None, 100], ['POP', 'Common', 8, None, 100], ['ALE', 'Common', 23, None, 60],
                      ['GIN', 'Preferred', 8, 0.02, 100], ['JOE', 'Common', 13, None, 250]]

        self.market.stocks.loadStockData(stock_list)
        self.market.addTrade("TEA", "Buy", 100, 50)
        self.market.addTrade("POP", "Buy", 90, 40)
        self.market.addTrade("ALE", "Buy", 80, 30)
        self.market.addTrade("GIN", "Buy", 70, 20)
        self.market.addTrade("JOE", "Buy", 60, 10)

        self.APIRoutes = APIRoutes(self.app, self.market)
        self.client = TestClient(self.app)

    def testTradeAPI(self):
        params = {
            "ticker": "JOE",
            "order_type": "sell",
            "quantity": 100,
            "price": 500
        }
        response = self.client.post("/trade", params=params)
        assert response.status_code == 200
        assert response.json() == {"Ticker": "JOE", "Response": "Trade Successful"}

    def testGetIndexAPI(self):
        response = self.client.get("/index/")
        assert response.status_code == 200
        assert response.json() == {"Index": "26.051710846973524"}

    def testDividendAPI(self):
        params = {
            "ticker": "GIN",
            "price": 20
        }

        response = self.client.get("/stocks/divyield", params=params)

        assert response.status_code == 200
        assert response.json() == {'Ticker': 'GIN', 'Div Yield': '5.0'}

    def testVWAPAPI(self):
        params = {
            "ticker": "JOE",
        }
        response = self.client.get("/stocks/vwap", params=params)

        assert response.status_code == 200
        assert response.json() == {'Ticker': 'JOE', 'VWAP:': '10.0'}

    def testPerAPI(self):
        params = {
            "ticker": "GIN",
            "price": 20
        }
        response = self.client.get("/stocks/per", params=params)

        assert response.status_code == 200
        assert response.json() == {'Ticker': 'GIN', 'P/E Ratio:': '2.5'}

    def testBadTickerAPI(self):

        params = {
            "ticker": "BAD",
        }

        response = self.client.get("/stocks/vwap", params=params)
        assert response.status_code == 200
        assert response.json() == {
                    "Ticker": "BAD",
                    "Response": "Ticker doesn't exist"}

        params = {
            "ticker": "BAD",
            "price": 20
        }

        response = self.client.get("/stocks/per", params=params)
        assert response.status_code == 200
        assert response.json() == {
                    "Ticker": "BAD",
                    "Response": "Ticker doesn't exist"}

        response = self.client.get("/stocks/divyield", params=params)
        assert response.status_code == 200
        assert response.json() == {
                    "Ticker": "BAD",
                    "Response": "Ticker doesn't exist"}

        params = {
            "ticker": "BAD",
            "order_type": "sell",
            "quantity": 100,
            "price": 500
        }
        response = self.client.post("/trade", params=params)

        assert response.status_code == 200
        assert response.json() == {'Ticker': 'BAD', 'Response': 'Invalid parameters'}

if __name__ == '__main__':
    unittest.main()
