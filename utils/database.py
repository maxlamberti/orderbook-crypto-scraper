import boto3
import logging
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

	def write(self, obook):
		logger.info("Writing orderbook for pair=%s, timestamp=%s to dynamodb.",
					obook.get('pair'), obook.get('timestamp'))
		self.put_item(obook)
