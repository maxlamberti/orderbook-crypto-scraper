import boto3
import logging
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class DynamoConnector:

	def __init__(self, region, table):
		self.region = region
		self.table_name = table
		dynamodb = boto3.resource('dynamodb', region_name=region)
		self.table = dynamodb.Table(table)

	def put_item(self, item):
		try:
			self.table.put_item(Item=item)
		except ClientError:
			logger.error("Failed putting item into dynamodb table %s.", self.table_name, exc_info=True)
		return item

	def get_item(self, search_key):
		item = {}
		try:
			response = self.table.get_item(Key=search_key)
			item = response.get('Item', {})
		except ClientError:
			logger.error(
				"Failed getting item from dynamodb table %s and search key %s",
				self.table_name, search_key, exc_info=True
			)
		return item

	def update_item(self, search_key, update_expression, attribute_values):
		try:
			self.table.update_item(
				Key=search_key,
				UpdateExpression=update_expression,
				ExpressionAttributeValues=attribute_values
			)
		except ClientError:
			logger.error(
				"Failed updating item in dynamodb table %s and search key %s",
				self.table_name, search_key, exc_info=True
			)


class OrderBookTable(DynamoConnector):

	def write(self, ob):
		logger.info("Writing orderbook for pair=%s, timestamp=%s to dynamodb.",
					ob.get('pair'), ob.get('timestamp'))
		self.put_item(ob)

	def get_orderbook(self, pair, ti=None, tf=None):
		"""Performs a scan operation on the database to return scraped order books.

		Parameters
		----------
		pair : str
			Currency pair for which to get order book data.
		ti : int
			Initial timestamp for range based query. (optional)
		tf : int
			Final timestamp for range based query. (optional)

		Returns
		-------
		list
			List of dicts of order book data.

		"""

		fe = Key('timestamp').between(ti, tf) & Key('pair').eq(pair)
		scan = self.table.scan(FilterExpression=fe)

		return scan.get('Items', [])
