import getData
import getPrices
import datetime
import time 
import csv
import math
from dotenv import load_dotenv
load_dotenv()

def getTime():
	
	now = datetime.datetime.now()
	now = now.strftime("%H:%M:%S")

	return now

def getDate():

	now = datetime.datetime.now()
	now = now.strftime("%d/%m/%Y")

	return now

def getHour():

	now = datetime.datetime.now()
	hour = now.strftime("%H")

	return hour

def writeToFile(operation, stock, price):

	with open('prices.csv', 'a', newline='') as csvfile:
	    spamwriter = csv.writer(csvfile, delimiter=',')
	    spamwriter.writerow([getDate()] + [operation] + [stock] + [price])

def calcSize(balance, price):
	partition = balance/3
	size = math.floor(partition/price)

	return size

def main():

	recommendations = list(getData.recommendations())
	recommendations = recommendations[:3]
	
	top3 = recommendations[0:3]

	print("Prices at " + getTime())
	for stock in top3:

		price = getPrices.getPrice(stock + '.AX')
		writeToFile('BUY', stock, price)
		print(stock, "$" + str(price))

		# place trade
		ig_service = trade.login()
		balance = trade.fetchBalance(ig_service)
		size = calcSize(balance, price)
		trade.placeTrade(ig_service, stock, size)

	print("Waiting to sell")
	time.sleep(60*40)

	print("Prices at " + getTime())
	for stock in top3:
		price = getPrices.getPrice(stock + '.AX')
		writeToFile('SELL', stock, price)
		print(stock, "$" + str(price))

	ig_service = login()
	trade.closePositions(ig_service)

if __name__ == "__main__":

	main()



