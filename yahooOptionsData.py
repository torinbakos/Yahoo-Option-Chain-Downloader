import urllib.request
import json
from datetime import date
from datetime import datetime
from pymongo import MongoClient

# this class will convert dates to strings in standard format for ease of access,
# but maintain unix time stamps within each individual contract
# the goal here is to lower overhead well populating the database

class getOptionsData:
    def __init__(self, databaseName: str):
        self.databaseName = databaseName
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[self.databaseName]

    def populateDatabase(self, ticker: str):
        # First URL request to get expiration dates
        url = urllib.request.urlopen(f"https://query2.finance.yahoo.com/v7/finance/options/{ticker}")
        requestData = json.loads(url.read().decode())
        expirationDates = requestData['optionChain']['result'][0]['expirationDates']
        # Build out / Access MongDB Collection for ticker
        currentTickerDocument = self.db[ticker]

        # create the building block data structs to insert into database
        calls, puts = {}, {}
        # using the list of expiration dates get the full option chain
        # the dict keys are teh dates of expiration for the contracts
        for d in expirationDates:
            url = urllib.request.urlopen(f"https://query2.finance.yahoo.com/v7/finance/options/{ticker}?date={str(d)}")
            calls[str(datetime.utcfromtimestamp(d).date())] = requestData['optionChain']['result'][0]['options'][0]['calls']
            puts[str(datetime.utcfromtimestamp(d).date())] = requestData['optionChain']['result'][0]['options'][0]['puts']

        # build out data struct to insert
        dataToInsert = {
            '_id' : date.today().strftime(("%Y-%m-%d")),
            'stats' : requestData['optionChain']['result'][0]['quote'],
            'options' : {
                'calls' : calls,
                'puts': puts
            }
        }

        # update the database Collection with struct dataToInsert
        # assert isinstance(currentTickerDocument.insert_one(dataToInsert).inserted_id, object)
        currentTickerDocument.insert_one(dataToInsert).inserted_id


