import yfinance as yf

def getPrice(ticker):

	stock = yf.Ticker(ticker)

	info = stock.info

	price = info['regularMarketPrice']

	return price