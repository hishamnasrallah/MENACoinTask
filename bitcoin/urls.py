from django.urls import re_path

from bitcoin.apis.views import BitCoinUSDPriceAPIView

urlpatterns = [
    re_path('v1/price/', BitCoinUSDPriceAPIView.as_view(), name='bitcoin_usd_price'),
]
