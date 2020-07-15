import configparser
from utils.utils import bool_from_str

config = configparser.ConfigParser()
config.read('settings.ini')

account_id = config['oanda']['account_id']
access_token = config['oanda']['access_token']
product_code = config['oanda']['product_code']

db_name = config['db']['name']
db_driver = config['db']['driver']

web_port = config['web']['port']

trade_duration = config['pytrading']['trade_duration'].lower()
back_test = bool_from_str(config['pytrading']['back_test'])
use_percent = float(config['pytrading']['use_percent'])
past_period = int(config['pytrading']['past_period'])
stop_limit_percent = float(config['pytrading']['stop_limit_percent'])
num_ranking = int(config['pytrading']['num_ranking'])

