import StockMarket
import fastapi
from Api import APIRoutes
import logging

if __name__ == "main":

    logging.basicConfig(level=logging.CRITICAL) #Could pass as parameter
    app = fastapi.FastAPI()
    market = StockMarket.StockMarket("GBCE")
    market.stocks.loadStockDataFromCSV("data/gbce_stock_data")
    routes = APIRoutes(app, market)






