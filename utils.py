from django.conf import settings
import requests



class AlphaVantageHelper:

    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY

    def exchange(self, function, _from_currency, _to_currency):
        alpha_vantage_end_point = settings.ALPHA_VANTAGE_EXCHANGE_END_POINT.format(
            function,
            _from_currency,
            _to_currency,
            self.api_key
        )
        response = requests.request("GET", alpha_vantage_end_point,).json()

        return response
