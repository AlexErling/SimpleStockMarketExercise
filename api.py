import json
import fastapi


class APIRoutes:

    def __init__(self, app: fastapi.FastAPI(), stock_market):
        self.app = app
        self.stock_market = stock_market

        @self.app.get("/index/")
        async def getIndex():
            result = self.stock_market.calcIndex()
            if result == float("nan"):
                return {"Response: Unable to calculate index. One or more stocks currently do not have trade data."}
            return {"Index": json.dumps(result)}

        @self.app.get("/stocks/per/")
        async def getPER(ticker: str, price: float):
            result = self.stock_market.stocks.getStockPER(ticker, price)
            if result == -1:
                return {
                    "Ticker": ticker,
                    "Response": "Ticker doesn't exist"}
            else:
                return {
                    "Ticker": ticker,
                    "P/E Ratio:": json.dumps(result)}

        @self.app.get("/stocks/vwap/")
        async def getVWAP(ticker: str):
            result = self.stock_market.stocks.getStockVWAP(ticker)
            if result == -1:
                return {
                    "Ticker": ticker,
                    "Response": "Ticker doesn't exist"}
            else:
                return {
                    "Ticker": ticker,
                    "VWAP:": json.dumps(result)}

        @self.app.get("/stocks/divyield/")
        async def getDividend(ticker: str, price: float):
            result = self.stock_market.stocks.getStockDividendYield(ticker, price)
            if result == -1:
                return {
                    "Ticker": ticker,
                    "Response": "Ticker doesn't exist"}
            else:
                return {
                    "Ticker": ticker,
                    "Div Yield": json.dumps(result)}

        @self.app.post("/trade")
        async def postTrade(ticker: str, order_type: str, quantity: float, price: float):
            result = self.stock_market.addTrade(ticker, order_type, quantity, price)
            if result == -1:
                return {
                    "Ticker": ticker,
                    "Response": "Invalid parameters"}
            else:
                return {
                    "Ticker": ticker,
                    "Response": "Trade Successful"}
