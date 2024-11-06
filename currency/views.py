from django.http import JsonResponse
from django.views import View
import requests
import time

from currency.models import ExchangeRate


class CurrentUSDView(View):
    @staticmethod
    def get_current_usd():
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        data = response.json()
        return data['rates']['RUB']

    def get(self, request):
        usd_to_rub = self.get_current_usd()

        # Сохранение курса в базе данных
        ExchangeRate.objects.create(rate=usd_to_rub)

        # Получение последних 10 курсов из базы данных
        last_requests = ExchangeRate.objects.order_by('-created_at')[:10]

        # Задержка между запросами
        time.sleep(10)

        return JsonResponse({
            'current_usd_to_rub': usd_to_rub,
            'last_requests': [
                {'rate': request.rate, 'created_at': request.created_at} for request in last_requests
            ]
        })
