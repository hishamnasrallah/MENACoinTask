from django.contrib import admin

# Register your models here.
from bitcoin.models import CurrencyExchangeRateLog


@admin.register(CurrencyExchangeRateLog)
class CurrencyExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_currency_code', 'to_currency_code', 'exchange_rate', 'last_refreshed')

