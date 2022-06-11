import StockMarket
import fastapi
import json
import logging

logging.basicConfig(level=logging.INFO)
stock_market = StockMarket.StockMarket("GBCE")
stock_market.stocks.loadStockDataFromCSV("data/gbce_stock_data")
app = fastapi.FastAPI()


@app.get("/index/")
async def getIndex():
    result = stock_market.calcIndex()
    if result == float("nan"):
        return {"Response: Unable to calculate index. One or more stocks currently do not have trade data."}
    return {"Index": json.dumps(result)}


@app.get("/stocks/per/")
async def getPER(ticker: str = "", price: float = 0):
    result = stock_market.stocks.getStockPER(ticker, price)
    if result == -1:
        return {"Response": "Ticker doesn't exist"}
    else:
        return {
            "Ticker": ticker,
            "P/E Ratio:": json.dumps(result)}


@app.get("/stocks/vwap/")
async def getVWAP(ticker: str = ""):
    result = stock_market.stocks.getStockVWAP(ticker)
    if result == -1:
        return {
            "Ticker": ticker,
            "Response": "Ticker doesn't exist"}
    else:
        return {
            "Ticker": ticker,
            "VWAP:": json.dumps(result)}


@app.get("/stocks/divyield/")
async def getDividend(ticker: str = "", price: float = 0):
    result = stock_market.stocks.getStockDividendYield(ticker, price)
    if result == -1:
        return {
            "Ticker": ticker,
            "Response": "Ticker doesn't exist"}
    else:
        return {
            "Ticker": ticker,
            "Response:": json.dumps(result)}


@app.post("/trade")
async def postTrade(ticker: str, order_type: str, quantity: float, price: float):
    result = stock_market.addTrade(ticker, order_type, quantity, price)
    if result == -1:
        return {
            "Ticker": ticker,
            "Response": "Invalid parameters"}
    else:
        return {
            "Ticker": ticker,
            "Response": "Trade Successful"}

