# Yahoo Option Chain Downloader
 A program to download the option chains from yahoo finance on a per ticker basis and then store that data in a MongoDB database.



Here is an example of how you might go about initializing and or connecting to a MongoDB database (Note the class is set to a local instance of MongoDB).
After which you may create and or connect to a container in that database named after the ticker you wish to collect data on.
The container will be automatically populated with that day's option data. 
Setting this up to run every day on a list of tickers of interest provides a simple free way to create a historical option chain database.

test = getOptionsData("yahooParser") # OptionChainData
test.populateDatabase('F') # Ticker