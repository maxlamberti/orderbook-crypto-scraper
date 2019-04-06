import os
import time
import krakenex
import logging.config

from pymongo import MongoClient
from utils.processing import query_order_book, mongo_reformat_orderbook
from config import LOGGING, PAIRS, DEPTHS


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('scraper')


MONGO_IP =  os.environ.get('MONGO_IP')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


kraken = krakenex.API()
client = MongoClient(MONGO_IP, username=DB_USER, password=DB_PASSWORD)
db = client.get_database('orderbooks')


def scraper(event=None, context=None):
	"""Target function for scheduled data scraping event.

	Parameters
	----------
	event : dict
		AWS Lambda uses this parameter to pass in event data to the handler.
	context : LambdaContext
		AWS Lambda uses this parameter to provide runtime information to your handler.

	"""

	start_time = time.time()

	for idx, pair in enumerate(PAIRS):

		ob = query_order_book(kraken, pair, DEPTHS[idx])
		item = mongo_reformat_orderbook(ob, pair)
		if item:
			result = db[pair].insert_one(item)
			logger.info("Insert status: {}".format(result))

		time.sleep(1)

	logger.info("Finished executing handler, took %0.1f seconds.", time.time() - start_time)
