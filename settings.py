import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

account_id = config['oanda']['account_id']
access_token = config['oanda']['access_token']
