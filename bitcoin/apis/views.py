from django.conf import settings
from django.utils.timezone import now
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from bitcoin.apis.serializers import BitCoinUSDPriceSerializer
from bitcoin.models import CurrencyExchangeRateLog
from bitcoin.tasks import check


class BitCoinUSDPriceAPIView(GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = BitCoinUSDPriceSerializer
    http_method_names = ['get', 'post']

    def get(self, request):
        try:
            current_price = CurrencyExchangeRateLog.objects.latest('last_refreshed')
            serializer = BitCoinUSDPriceSerializer(current_price)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "There is no data yet."}, status=status.HTTP_404_NOT_FOUND)





    def post(self, request):
        exchange = check.delay()
        if exchange.status_code == 200:
            return Response(exchange.json(), status=status.HTTP_200_OK)
        else:
            return Response(exchange.json(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # the following method for update the schedule of the periodic task
    # def check_intervals(self, data):
    #     if not IntervalSchedule.objects.filter(every=data['interval']['every'],
    #                                            period=data['interval']['period']).exists():
    #
    #         interval_schedule = IntervalSchedule.objects.create(every=data['interval']['every'],
    #                                                             period=data['interval']['period'])
    #     else:
    #         interval_schedule = IntervalSchedule.objects.filter(every=data['interval']['every'],
    #                                                             period=data['interval']['period']).first()
    #     return interval_schedule
    #
    # def put(self, request, *args, **kwargs):
    #
    #     interval_schedule_obj = self.check_intervals(request.data)
    #
    #     if PeriodicTask.objects.filter(name='check_exchange_rate').exists():
    #         check_exchange_rate_obj = PeriodicTask.objects.filter(name='check_exchange_rate').first()
    #         check_exchange_rate_obj.interval = interval_schedule_obj
    #         check_exchange_rate_obj.save()
    #
    #     else:
    #
    #         check_exchange_rate_obj = PeriodicTask.objects.create(name='check_exchange_rate',
    #                                                               task='bitcoin.tasks.check',
    #                                                               interval=interval_schedule_obj,
    #                                                               start_time=now())
    #     return Response(status=status.HTTP_200_OK)
