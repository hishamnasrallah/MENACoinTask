from rest_framework import serializers


class BitCoinUSDPriceSerializer(serializers.Serializer):
    # country = CountryField()
    class Meta:
        fields = ('function', 'from_currency', 'to_currency')