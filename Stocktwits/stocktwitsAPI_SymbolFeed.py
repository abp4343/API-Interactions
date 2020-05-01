import urllib.request, urllib.parse
import ssl
import json
from datetime import datetime
from dateutil import parser
from pytz import timezone
'''

Description: 	Returns the most recent 30 (default) messages for the specified symbol. 
				Includes symbol object in response.

Use URL: 		https://api.stocktwits.com/api/2/streams/symbol/:id.json

Parameters:

id:				Ticker symbol, Stock ID, or RIC code of the symbol (Required)
since:			Returns results with an ID greater than (more recent than) the specified ID.
max:			Returns results with an ID less than (older than) or equal to the specified ID.
limit:			Default and max limit is 30. This limit must be a number under 30.
callback:		Define your own callback function name, add this parameter as the value.
filter:			Filter messages by links, charts, videos, or top. (Optional)

'''

optionalParams = {'since' : None, 'max' : None, 'limit' : 5,
				'callback' : None, 'filter' : None}

#urlencode params that have been altered
params = {key : value for (key, value) in optionalParams.items() if value != None}
paramData = urllib.parse.urlencode(params).encode('utf-8')

#Bypass SSL Certificate Errors
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


while True:
	stockSymbol = input("Enter stock symbol:\t")

	if(len(stockSymbol) < 1):
		break

	baseUrl = "https://api.stocktwits.com/api/2/streams/symbol/"\
			+ stockSymbol.upper() + ".json"

	print("Retrieving", baseUrl + "...\n\n\n")

	try:
		connectionObj = urllib.request.Request(baseUrl, data = paramData, headers = {'User-Agent' : 'Magic'})
		connection = urllib.request.urlopen(connectionObj, context = context)

	except:
		print("Invalid Stock Symbol...\n\n")
		continue

	stockData = connection.read().decode()
	headers = dict(connection.getheaders())

	#get messages: username, full name, user message, and date
	est = timezone('US/Eastern')
	fmt = '%Y-%m-%d %H:%M:%S %Z%z'

	readData = json.loads(stockData)

	for message in readData['messages']:

		print("Username:", message['user']['username'])
		print("Name:", message['user']['name'])
		print("Message:", message['body'])

		messageTime = parser.parse(message['created_at'])
		print("Time of Message:", messageTime.astimezone(est).strftime(fmt))

		print("\n\n\n")





