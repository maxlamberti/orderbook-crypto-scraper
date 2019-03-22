import time
import krakenex
import logging.config

from utils.database import OrderBookTable
from utils.processing import query_order_book, reformat_orderbook
from config import PAIRS, AWS_REGION, NUM_ORDERS, TABLE, LOGGING


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('scraper')


kraken = krakenex.API()
db = OrderBookTable(AWS_REGION, TABLE)


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

		ob = query_order_book(kraken, pair, NUM_ORDERS[idx])
		item = reformat_orderbook(ob, pair)
		if item:
			db.write(item)

	logger.info("Finished executing handler, took %0.1f seconds.", time.time() - starttime)
