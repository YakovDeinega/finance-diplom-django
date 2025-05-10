from django.conf import settings
from requests import Response

from common_utils.api import BaseAPIService


class MOEXAPIService(BaseAPIService):
    host = settings.SERVICE_URLS['MOEX_SERVICE_URL']
    api_path = 'iss/'
    token = settings.SERVICE_TOKENS['MOEX_SERVICE_TOKEN']

    @classmethod
    def get_trade_statictics_for_actions(cls, ticker: str = '') -> Response:
        """Торговая статистика по всем акциям или по одной указанной на текущий день.

        :param ticker: Код ценной бумаги, например 'SBER'
        :return: Объект Response
        """
        additional_url = f'/{ticker}' if ticker else ''
        return cls.get(f'engines/stock/markets/shares/boards/tqbr/securities{additional_url}.json')

    @classmethod
    def get_candles_for_action(cls, ticker: str, dt_from: str, dt_till: str, interval: int = 10) -> Response:
        """Свечи по одной указанной акции.

        :param ticker: Код ценной бумаги, например 'SBER'
        :param dt_from: Дата начала периода, например '2024-03-01'
        :param dt_till: Дата окончания периода, например '2024-05-01'
        :param interval: Период свечей
        :return: Объект Response
        """
        return cls.get(
            (
                f'engines/stock/markets/shares/boards/tqbr/securities/{ticker}/candles.json'
                f'?from={dt_from}&till={dt_till}&interval={interval}'
            ),
        )

    @classmethod
    def get_orderbook_for_action(cls, ticker: str) -> Response:
        """Стакан котировок по одной указанной акции.

        :param ticker: Код ценной бумаги, например 'SBER'
        :return: Объект Response
        """
        return cls.get(f'engines/stock/markets/shares/boards/tqbr/securities/{ticker}/orderbook.json')

    @classmethod
    def get_trades_for_action(cls, ticker: str, tradeno: int) -> Response:
        """Стакан котировок по одной указанной акции.

        :param ticker: Код ценной бумаги, например 'SBER'
        :param tradeno: Получить сделки, которые идут начиная с указанного номера
        :return: Объект Response
        """
        return cls.get(f'engines/stock/markets/shares/boards/tqbr/securities/{ticker}/trades.json?tradeno={tradeno}')

