

PAIRS = ["XXRPZEUR"]
DEPTHS = [200]

LOGGING = {
	'disable_existing_loggers': False,
	'version': 1,
	'formatters': {
		'simple': {
			'format': '%(asctime)s - %(levelname)s - %(message)s'
		},
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'formatter': 'simple',
			'class': 'logging.StreamHandler',
		}
	},
	'loggers': {
		'scraper': {
			'handlers': ['console'],
			'level': 'INFO',
		}
	},
}
