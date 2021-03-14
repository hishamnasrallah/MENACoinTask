from django.conf import settings
from django.utils.timezone import now
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from bitcoin.apis.serializers import BitCoinUSDPriceSerializer
from bitcoin.tasks import check
from utils import AlphaVantageHelper


class BitCoinUSDPriceAPIView(GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = BitCoinUSDPriceSerializer
    http_method_names = ['get', 'post', 'put']

    def get(self, request):

        exchange = AlphaVantageHelper().exchange(function='CURRENCY_EXCHANGE_RATE', _from_currency='BTC',
                                                 _to_currency='USD')
        return Response(exchange, status=status.HTTP_200_OK)


    def post(self, request):

        exchange = check()
        return Response(exchange, status=status.HTTP_200_OK)

    def check_intervals(self, data):
        if not IntervalSchedule.objects.filter(every=data['interval']['every'],
                                               period=data['interval']['period']).exists():

            interval_schedule = IntervalSchedule.objects.create(every=data['interval']['every'],
                                                                period=data['interval']['period'])
        else:
            interval_schedule = IntervalSchedule.objects.filter(every=data['interval']['every'],
                                                                period=data['interval']['period']).first()
        return interval_schedule

    def put(self, request, *args, **kwargs):

        interval_schedule_obj = self.check_intervals(request.data)

        if PeriodicTask.objects.filter(name='check_exchange_rate').exists():
            check_exchange_rate_obj = PeriodicTask.objects.filter(name='check_exchange_rate').first()
            check_exchange_rate_obj.interval = interval_schedule_obj
            check_exchange_rate_obj.save()

        else:

            check_exchange_rate_obj = PeriodicTask.objects.create(name='check_exchange_rate',
                                                                  task='bitcoin.tasks.check',
                                                                  interval=interval_schedule_obj,
                                                                  start_time=now())
        return Response(status=status.HTTP_200_OK)
