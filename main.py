import logging
import sys

import settings
import constants
from oanda.oanda import APIClient
from oanda.oanda import Order

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == '__main__':
    """
    print(settings.account_id)
    print(settings.access_token)
    print(settings.product_code)
    print(settings.db_name)
    print(settings.db_driver)
    print(settings.web_port)
    print(settings.trade_duration)
    print(settings.back_test)
    print(settings.use_percent)
    print(settings.past_period)
    print(settings.stop_limit_percent)
    print(settings.num_ranking)
    """
    api_client = APIClient(access_token=settings.access_token, account_id=settings.account_id)
    """
    balance = api_client.get_balance()
    print(balance.available)
    print(balance.currency)

    ticker = api_client.get_ticker(product_code='USD/JPY')
    print(ticker.product_code)
    print(ticker.timestamp)
    print(ticker.bid)
    print(ticker.ask)
    print(ticker.volume)

    print(ticker.truncate_date_time('5s'))
    print(ticker.truncate_date_time('1m'))
    print(ticker.truncate_date_time('1h'))
    print(ticker.mid_price)
    print(ticker.volume)

    from functools import partial

    def trade(ticker):
        print(ticker.mid_price)
        print(ticker.ask)
        print(ticker.bid)

    callback = partial(trade)
    api_client.get_realtime_ticker(callback)
    """
    order = Order(
        product_code=settings.product_code,
        side=constants.BUY,
        units=10
    )
    api_client.send_order(order)


