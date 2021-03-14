from __future__ import absolute_import, unicode_literals

from decimal import Decimal

from celery import shared_task

from utils import AlphaVantageHelper
from bitcoin.models import CurrencyExchangeRateLog


@shared_task()
def check():
    exchange = AlphaVantageHelper().exchange(function='CURRENCY_EXCHANGE_RATE', _from_currency='BTC',
                                             _to_currency='USD')
    obj_response_value = exchange['Realtime Currency Exchange Rate']
    from_currency_code = obj_response_value['1. From_Currency Code']
    from_currency_name = obj_response_value['2. From_Currency Name']
    to_currency_code = obj_response_value['3. To_Currency Code']
    to_currency_name = obj_response_value['4. To_Currency Name']
    exchange_rate = Decimal(obj_response_value['5. Exchange Rate'])
    last_refreshed = obj_response_value['6. Last Refreshed']
    time_zone = obj_response_value['7. Time Zone']
    bid_price = Decimal(obj_response_value['8. Bid Price'])
    ask_price = Decimal(obj_response_value['9. Ask Price'])

    CurrencyExchangeRateLog.objects.create(from_currency_code=from_currency_code,
                                           from_currency_name=from_currency_name,
                                           to_currency_code=to_currency_code,
                                           to_currency_name=to_currency_name,
                                           exchange_rate=exchange_rate,
                                           last_refreshed=last_refreshed,
                                           time_zone=time_zone,
                                           bid_price=bid_price,
                                           ask_price=ask_price
                                           )
    return exchange