from django.conf import settings
from requests import Response

from common_utils.api import BaseAPIService


class MLAPIService(BaseAPIService):
    host = settings.SERVICE_URLS['ML_SERVICE_URL']
    api_path = ''
    token = settings.SERVICE_TOKENS['ML_SERVICE_TOKEN']

    @classmethod
    def predict(cls, ticker, data) -> Response:
        """Предсказать цены закрытия свечей на следующие 20 часов.

        :param ticker: Код ценной бумаги, например 'SBER'.
        :param data: Цены закрытия свечей за предыдущие 20 часов.
        :return: Объект Response.
        """
        print(data)
        return cls.post(f'predict/{ticker}', json=data)

