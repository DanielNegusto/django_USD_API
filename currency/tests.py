import pytest
from django.urls import reverse
from rest_framework import status
from currency.models import ExchangeRate
from unittest.mock import patch


@pytest.mark.django_db
class TestCurrentUSDView:

    @patch('currency.views.requests.get')
    def test_get_current_usd(self, mock_get, client):
        # Настройка mock-ответа
        mock_get.return_value.json.return_value = {
            'rates': {
                'RUB': 75.0,  # Пример курса
            }
        }

        # Выполнение GET-запроса к представлению
        response = client.get(reverse('current_usd'))  # Замените 'current_usd' на имя вашего URL

        # Проверка статуса ответа
        assert response.status_code == status.HTTP_200_OK

        # Проверка содержания ответа
        assert response.json()['current_usd_to_rub'] == 75.0

        # Проверка сохранения курса в базе данных
        assert ExchangeRate.objects.count() == 1
        assert ExchangeRate.objects.first().rate == 75.0

        # Проверка, что последние запросы возвращаются корректно
        last_requests = response.json()['last_requests']
        assert len(last_requests) == 1
        assert last_requests[0]['rate'] == 75.0
