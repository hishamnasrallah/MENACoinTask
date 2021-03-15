from rest_framework import serializers

from bitcoin.models import CurrencyExchangeRateLog


class BitCoinUSDPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyExchangeRateLog
        fields = ('from_currency_code', 'to_currency_code', 'exchange_rate', 'bid_price', 'ask_price')