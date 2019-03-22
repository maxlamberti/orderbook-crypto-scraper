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

	def get_strategy(self, strategy_id):
		search_key = {'strategy_id': strategy_id}
		item = self.get_item(search_key)
		return item

	def add_order_id(self, strategy_id, txid):
		logger.info("Adding %s to %s strategy config.", txid, strategy_id)
		search_key = {'strategy_id': strategy_id}
		update_expression = "SET orders = list_append(orders, :id)"
		attribute_values = {':id': [txid]}
		self.update_item(search_key, update_expression, attribute_values)
