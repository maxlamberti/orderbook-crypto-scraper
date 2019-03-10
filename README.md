# Cloud scraper for cryptocurrency order book data.
![python version](https://img.shields.io/badge/python-3.6-blue.svg)

Create an event schedule to scrape order book data from a public exchange API (here implemented with [Kraken API](https://www.kraken.com/help/api)), compresses it into relevant features, and insert it into a private database. The scraper is hosted serverless on AWS Lambda making it virtually free to run.

# Resources
- [Kraken visualization of their data](https://support.kraken.com/hc/en-us/articles/115000364388-Trading-Glossary)
- [Kraken API](https://www.kraken.com/help/api)

## Tech
- [Zappa](https://github.com/Miserlou/Zappa) - deploy Python Lambdas and schedule events
- [krakenex](https://github.com/veox/python3-krakenex) - API for Kraken exchange
- [AWS Lambda](https://aws.amazon.com/lambda/) - serverless compute service
- [AWS RDS](https://aws.amazon.com/rds/) - relational database service

## Installation and Setup

### Clone
Clone this repo to your local machine. 
```
$ git clone https://github.com/hexamax/orderbook-crypto-scraper.git
```

### Install Requirements
Zappa requires an active [virtual environment](https://virtualenv.pypa.io/en/latest/installation/) to deploy. Either install and activate your own virtual environment or execute the following steps.
```
$ cd ohlc-crypto-scraper
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Configure Database
Write your database credentials into the corresponding fields of the database configuration file located at `ohlc-crypto-scraper/db_config.py`

**WARNING**: The scraper was written, used and tested for a PostgreSQL database only. For compatability make sure to be running a Postgres instance as well. To set up a low cost RDS Postgres instance on AWS check out this [tutorial](https://aws.amazon.com/getting-started/tutorials/create-connect-postgresql-db/).

### Zappa Settings (Optional)
The `zappa_settings.json` file was initialized with some sensible defaults and will run fine without additional manipulation. However, here are some easy changes you can make to customize your deploy:
- Specify the rate at which the data scraping event is executed by changing the [rate expression](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#RateExpressions) located in `zappa_settings.json > events > expression`.
- Specify the [aws region](https://docs.aws.amazon.com/general/latest/gr/rande.html) of your deploy in the `aws_region` field.
- Specify a custom name for your S3 bucket using the `s3_bucket` field.

## Deploy and Schedule

### Initial Deploy
Use the following command for the initial deploy only.
```
$ zappa deploy scrape_event
```
Zappa will spit out the deployment information to your terminal and let you know if the deploy was succesfull. If the deploy was succesfull your data scraper should now be up and running.

Subsequent deploys are possible by calling zappa update.
```
$ zappa update scrape_event
```

### Schedule
If you decided to change the rate expression in the `zappa_settings.json` file you can easily reschedule your scraper.
```
$ zappa schedule scrape_event
```

### Undeploy
This will remove the Lambda function.
```
$ zappa undeploy scrape_event
```

## Logs
You can monitor your scraper's AWS CloudWatch logs directly from the console.
```
$ zappa tail scrape_event
```
