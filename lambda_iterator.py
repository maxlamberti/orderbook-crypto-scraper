import os
import time
import boto3
import logging.config
from config import LOGGING


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('iterator')


lambda_client = boto3.client('lambda')


LAMBDA_NAME = os.environ.get('LAMBDA_TARGET')  # name of lambda scraper
TIMEOUT = int(os.environ.get('TIMEOUT'))  # seconds
N_SAMPLES = int(os.environ.get('N_SAMPLES'))  # samples per timeout period


def iterator(event=None, context=None):
	"""Spaces out lambda invocations for scrape events.

	Cloudwatch event scheduling only allows sampling at minute frequency.
	This function is used to achieve sampling in sub-minute frequencies.

	Parameters
	----------
	event : dict
		AWS Lambda uses this parameter to pass in event data to the handler.
	context : LambdaContext
		AWS Lambda uses this parameter to provide runtime information to your handler.

	"""

	invoc_time = time.time()
	wait_time = float(TIMEOUT) / N_SAMPLES
	count = 0

	while (time.time() - invoc_time < TIMEOUT) and (count < N_SAMPLES):

		exec_start = time.time()
		count += 1

		try:
			_ = lambda_client.invoke(
				FunctionName=LAMBDA_NAME,
				InvocationType='Event'
			)
		except Exception as e:  # not sure which errors might be raised
			logger.error('Failed invoking lambda. Error: %s', e)

		exec_time = time.time() - exec_start
		logger.info("%sth lambda invocation took %s seconds.", count, exec_time)

		time.sleep(abs(wait_time - exec_time))
