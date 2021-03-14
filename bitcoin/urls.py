from django.urls import re_path

from bitcoin.apis.views import BitCoinUSDPriceAPIView

urlpatterns = [
    re_path('bitcoin_usd_price/', BitCoinUSDPriceAPIView.as_view(), name='bitcoin_usd_price'),
]
