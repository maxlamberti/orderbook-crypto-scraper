import os
import time
import krakenex
import logging.config

from utils.database import OrderBookTable
from utils.processing import query_order_book, reformat_orderbook
from config import LOGGING, PAIRS, DEPTHS


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('scraper')


env = os.environ.get('ENVIRONMENT')
awsregion = os.environ.get('DB_REGION')
table = os.environ.get('TABLE')


kraken = krakenex.API()
db = OrderBookTable(awsregion, table)


def scraper(event=None, context=None):
	"""Target function for scheduled data scraping event.

	Parameters
	----------
	event : dict
		AWS Lambda uses this parameter to pass in event data to the handler.
	context : LambdaContext
		AWS Lambda uses this parameter to provide runtime information to your handler.

	"""

	starttime = time.time()

	for idx, pair in enumerate(PAIRS):

		ob = query_order_book(kraken, pair, DEPTHS[idx])
		item = reformat_orderbook(ob, pair)
		if item:
			db.write(item)

	logger.info("Finished executing handler, took %0.1f seconds.", time.time() - starttime)
