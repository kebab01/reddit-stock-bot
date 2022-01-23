import requests
import praw
import csv
import re
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

day = "Market Open thread for General Trading"
perm = "Premarket Thread for General Trading and Plans"
weekend = "Weekend Thread for General Discussion and Plans"
site = "https://www.reddit.com/r/ASX_Bets/?f=flair_name%3A%22Daily%20Thread%22"

appID = os.getenv("APP_ID")
secret = os.getenv("SECRET")

# list of all stocks on the ASX
stockList = []
# list of all comments on subreddit
commentList = []
# wordlists to determain good or bad things are being said about stocks
wordListGood = []
wordListBad = []

recommendations = []

reddit = praw.Reddit(
    client_id=appID,
    client_secret=secret,
    user_agent=os.getenv("USERNAME"),
)

def getStocks():

	with open('ASX_Listed_Companies_28-04-2021_10-50-08_AEST.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		lineCount = 0
		for row in csv_reader:
			stockList.append(row[0])

def getComments():
	subID = ""
	for submission in reddit.subreddit("ASX_Bets").hot(limit=10):
	    title = submission.title
	    if title.find(perm) != -1:
	    	print("Thread:", title)
	    	subID = submission.id
	    	submission = reddit.submission(id=subID)
	    	comments = submission.comments.list()

	    elif title.find(day) != -1:
	    	print("Thread:", title)
	    	subID = submission.id
	    	submission = reddit.submission(id=subID)
	    	comments = submission.comments.list()

	# puts all comments in list
	print("Comments to be scanned", len(comments))
	for comment in comments:

		try:
			commentList.append(comment.body)
			num += 1
		except:
			pass

def getWordlists():
	with open ("good.txt", "r") as file:
		words = file.read().splitlines()

		for word in words:
			wordListGood.append(word)

	with open ("negative.txt", "r") as file:
		words = file.read().splitlines()

		for word in words:
			wordListBad.append(word)
    	
def recommendations():

	# discionary of stocks and amount of mentions that stocks has
	stockCount = {}

	now = datetime.datetime.now()
	print("\nCurrent date and time : ")
	print(now.strftime("%Y-%m-%d %H:%M:%S\n"))

	print("Loading stocks...")
	getStocks()

	print("Loading comments...")
	getComments()

	print("Loading wordlist...")
	getWordlists()

	#Stores comments where reference to stock is present for it to be written to file
	stockInComments = []

	# for every comment on thread
	for comment in commentList:
		# iterate through every stock on ASX to check for mention
		for stock in stockList:

			if comment.find(stock) != -1:
				
				stockInComments.append(str(comment))

				if stock not in stockCount:
					stockCount[stock] = 1

				elif stock in stockCount:
					stockCount[stock] += 1

				for word in wordListGood:
					comment = comment.lower()
					word = word.lower()

					if comment.find(word) != -1:
						stockCount[stock] += 2

				for word in wordListBad:
					comment = comment.lower()
					word = word.lower()
					if comment.find(word) != -1:
						stockCount[stock] -= 2.5

	stockCount = dict(sorted(stockCount.items(), key=lambda item: item[1], reverse = True))

	#write comments to file
	for comment in stockInComments:
		with open('comments.txt', 'a') as f:
			f.write(comment)

	try:
		del stockCount['ASX']
		del stockCount['BUY']
	except:
		pass

	for i in range(5):
		stock = list(stockCount)[i]
		print(stock, stockCount[stock])

	print(len(commentList), 'comments scanned')

	return stockCount

if __name__ == "__main__":

	recommendations()