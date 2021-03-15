from django.db import models

# Create your models here.


class CurrencyExchangeRateLog(models.Model):
    from_currency_code = models.CharField(max_length=3, null=True, blank=True)
    from_currency_name = models.CharField(max_length=50, null=True, blank=True)
    to_currency_code = models.CharField(max_length=3, null=True, blank=True)
    to_currency_name = models.CharField(max_length=50, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    last_refreshed = models.DateTimeField(null=True, blank=True)
    time_zone = models.CharField(max_length=30, null=True, blank=True)
    bid_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    ask_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
