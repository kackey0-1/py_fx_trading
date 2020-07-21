from datetime import datetime
import logging
import math
import dateutil.parser
from oandapyV20 import API
from oandapyV20.endpoints import accounts
from oandapyV20.endpoints import instruments
from oandapyV20.endpoints import orders
from oandapyV20.endpoints.pricing import PricingInfo
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20.exceptions import V20Error

import settings
from utils import constants
logger = logging.getLogger(__name__)


class Balance(object):
    def __init__(self, currency, available):
        self.currency = currency
        self.available = available


class Ticker(object):
    def __init__(self, product_code, timestamp, bid, ask, volume):
        self.product_code = product_code
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask
        self.volume = volume

    @property
    def mid_price(self):
        return (self.bid + self.ask) / 2

    @property
    def time(self):
        return datetime.utcfromtimestamp(self.timestamp)

    # 2020-01-02 03:04:27
    # 2020-01-02 03:04:25 5S
    # 2020-01-02 03:04:00 1M
    # 2020-01-02 03:00:00 1H
    def truncate_date_time(self, duration):
        ticker_time = self.time
        if duration == constants.DURATION_S5:
            new_sec = math.floor(self.time.second / 5) * 5
            ticker_time = datetime(self.time.year, self.time.month, self.time.day,
                                   self.time.hour, self.time.minute, new_sec)
            time_format = '%Y-%m-%d %H:%M:%S'
        elif duration == constants.DURATION_M1:
            time_format = '%Y-%m-%d %H:%M'
        elif duration == constants.DURATION_H1:
            time_format = '%Y-%m-%d %H'
        else:
            logger.warning('action=truncate_date_time error=no_datetime_format')
            return None

        str_date = datetime.strftime(ticker_time, time_format)
        return datetime.strptime(str_date, time_format)


class Order(object):
    def __init__(self, product_code, side, units, order_type='MARKET', order_state=None, filling_transaction_id=None):
        self.product_code = product_code
        self.side = side
        self.units = units
        self.order_type = order_type
        self.order_state = order_state
        self.filling_transaction_id=filling_transaction_id


class APIClient(object):
    def __init__(self, access_token, account_id, environment='practice'):
        self.access_token = access_token
        self.account_id = account_id
        self.client = API(access_token=access_token, environment=environment)

    def get_balance(self) -> Balance:
        req = accounts.AccountSummary(accountID=self.account_id)
        try:
            resp = self.client.request(req)
        except V20Error as e:
            logger.error(f'action=get_balance error={e}')
            raise
        available = float(resp['account']['balance'])
        currency = resp['account']['currency']
        return Balance(currency, available)

    def get_ticker(self, product_code) -> Ticker:
        params = {
            'instruments': product_code,
        }
        req = PricingInfo(accountID=self.account_id, params=params)
        try:
            resp = self.client.request(req)
        except V20Error as e:
            logger.error(f'action=get_ticker error={e}')
        print(resp)
        timestamp = datetime.timestamp(dateutil.parser.parse(resp['time']))
        prices = resp['prices'][0]
        instrument = prices['instrument']
        bid = float(prices['bids'][0]['price'])
        ask = float(prices['asks'][0]['price'])
        volume = self.get_candle_volume()
        return Ticker(product_code=instrument,
                      timestamp=timestamp,
                      bid=bid,
                      ask=ask,
                      volume=volume)

    def get_candle_volume(self, count=1, granularity=constants.TRADE_MAP[settings.trade_duration]['granularity']):
        params = {
            'count': count,
            'granularity': granularity
        }
        req = instruments.InstrumentsCandles(instrument=settings.product_code, params=params)
        try:
            resp = self.client.request(req)
        except V20Error as e:
            logger.error(f'action=get_candle_volume error={e}')
            raise
        print(resp)
        return int(resp['candles'][0]['volume'])

    def get_realtime_ticker(self, callback):
        req = PricingStream(accountID=self.account_id, params={
            'instruments': settings.product_code})
        try:
            for resp in self.client.request(req):
                if resp['type'] == 'PRICE':
                    print(resp)
                    timestamp = datetime.timestamp(dateutil.parser.parse(resp['time']))
                    instrument = resp['instrument']
                    bid = float(resp['bids'][0]['price'])
                    ask = float(resp['asks'][0]['price'])
                    volume = self.get_candle_volume()
                    ticker = Ticker(instrument, timestamp, bid, ask, volume)
                    callback(ticker)

        except V20Error as e:
            logger.error(f'action=get_realtime_ticker error={e}')
            raise



