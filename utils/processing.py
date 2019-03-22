import time
import logging.config
from decimal import Decimal
from requests import HTTPError


logger = logging.getLogger(__name__)


def query_order_book(api, pair, count):
	"""Queries the kraken order book.

	Parameters
	----------
	api : Kraken API Object
		A kraken api object to query for the orderbook data.
	pair : str
		Asset pair to get market depth for.
	count : int
		Maximum number of asks/bids

	Returns
	-------
	dict
		Kraken response with orderbook data. Empty dict if fails.
	"""

	try:
		response = api.query_public('Depth', {'pair': pair, 'count': count})
	except HTTPError:
		response = {}
		logger.error("Failed querying order book data for pair=%s.", pair)

	obook = response.get('result', {}).get(pair)

	return obook


def reformat_orderbook(obook, pair):
	"""Process the orderbook response for write to DynamoDB.

	Parameters
	----------
	obook : dict
		The kraken response returned by query_order_book(...).
	pair : str
		The currency pair denomination of the orderbook.

	Returns
	-------
	dict
		The orderbook in format for DynamoDB insertion. Returns empty dict on error.
	"""

	if not obook:
		item = {}
		logger.error("Orderbook for pair=%s is empty. Can't reformat for DB insertion.", pair)
	else:
		asks = []
		bids = []
		for order in obook['asks']:
			asks.append([Decimal(order[0]), Decimal(order[1]), order[2]])
		for order in obook['bids']:
			asks.append([Decimal(order[0]), Decimal(order[1]), order[2]])
		item = {
			'pair': pair,
			'timestamp': int(time.time()),
			'asks': asks,
			'bids': bids
		}

	return item
