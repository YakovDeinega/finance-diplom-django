import datetime

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse
from requests import HTTPError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from moex.create_functions import parse_securities_and_marketdata, parse_start_structure
from services.ml_fastapi import MLAPIService
from services.moex import MOEXAPIService
from moex.serializers import ActionTradeStatisticsResponseSerializer, ActionCandlesResponseSerializer, \
    ActionOrderBookResponseSerializer, ActionTradesResponseSerializer


# Create your views here.

class ActionTradeStatisticsGetAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ActionTradeStatisticsResponseSerializer

    @extend_schema(
        tags=['Real-time market data - Акции'],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Ошибка при запросе к MOEX API',
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string',
                            'example': 'Ошибка при запросе к MOEX API.'
                        },
                    },
                },
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description='Учетные данные не предоставлены',
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string',
                            'example': 'Authentication credentials were not provided.'
                        },
                    },
                },
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        },
        summary='Получить торговую статистику за сегодня по указанным акциям',
        description=(
            f'Возвращает торговую статистику за сегодня по указанным акциям, включая статические данные'
            f'и рыночные показатели, а именно: {serializer_class.Meta.description}'
        ),
        parameters=[
            OpenApiParameter(
                name='tickers',
                location=OpenApiParameter.QUERY,
                description='Нужные акции в формате перечисления идентификаторов ценных бумаг через запятую',
                examples=[
                    OpenApiExample(
                        'Акции Сбербанка, Инарктики, АстрЭнСб',
                        value='SBER,AQUA,ASSB',
                    ),
                ],
                type=str,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        tickers_string = request.query_params.get('tickers')
        tickers = tickers_string.split(',') if tickers_string else []
        ticker = tickers[0] if len(tickers) == 1 else ''

        response = MOEXAPIService.get_trade_statictics_for_actions(ticker)
        try:
            response.raise_for_status()
        except HTTPError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Ошибка при запросе к MOEX API'})

        result_data = parse_securities_and_marketdata(response.json())

        if len(tickers) > 1:
            result_data = [{'ticker': key, **result_data[key]} for key in sorted(tickers) if key in result_data]
        else:
            result_data = [{'ticker': key, **result_data[key]} for key in result_data]
        return Response(status=status.HTTP_200_OK, data=self.serializer_class(result_data, many=True).data)


class ActionCandlesGetAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ActionCandlesResponseSerializer

    @extend_schema(
        tags=['Real-time market data - Акции'],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Ошибка при запросе к MOEX API',
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string',
                            'example': 'Ошибка при запросе к MOEX API.'
                        },
                    },
                },
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description='Учетные данные не предоставлены',
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string',
                            'example': 'Authentication credentials were not provided.'
                        },
                    },
                },
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        },
        summary='Получить свечи по одной указанной акции за определенный период',
        description=(
            f'Возвращает свечи по одной указанной акции за определенный период (первые 500 записей), '
            f'включая:\n\n{serializer_class.Meta.description}'
        ),
        parameters=[
            OpenApiParameter(
                name='ticker',
                location=OpenApiParameter.PATH,
                description='Код ценной бумаги',
                examples=[
                    OpenApiExample(
                        'Акция Сбербанка',
                        value='SBER',
                    ),
                ],
                type=str,
                required=True,
            ),
            OpenApiParameter(
                name='from',
                location=OpenApiParameter.QUERY,
                description='Дата начала периода (формат YY-MM-DD)',
                examples=[
                    OpenApiExample(
                        '1-ое января 2025 года',
                        value='2025-01-01',
                    ),
                ],
                type=str,
                required=True,
            ),
            OpenApiParameter(
                name='till',
                location=OpenApiParameter.QUERY,
                description='Дата окончания периода (формат YY-MM-DD)',
                examples=[
                    OpenApiExample(
                        '1-ое марта 2025 года',
                        value='2025-03-01',
                    ),
                ],
                type=str,
                required=True,
            ),
            OpenApiParameter(
                name='interval',
                location=OpenApiParameter.QUERY,
                description=(
                    'Период свечей:\n\n- 1 - 1 мин;\n- 10 - 10 мин;\n - 60 - 1 час;\n - 24 - 1 день;\n'
                    ' - 7 - 1 неделя;\n - 31 - 1 месяц.'
                ),
                type=str,
                required=True,
                default=10,
            ),
        ],
    )
    def get(self, request, ticker, *args, **kwargs):
        dt_from = request.query_params.get('from')
        dt_till = request.query_params.get('till')
        interval = request.query_params.get('interval')
        if not dt_from or not dt_till or not interval:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': 'Не был представлен один или несколько параметров запроса'},
            )

        response = MOEXAPIService.get_candles_for_action(ticker, dt_from, dt_till, interval)

        try:
            response.raise_for_status()
        except HTTPError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Ошибка при запросе к MOEX API'})

        result_data = parse_start_structure(response.json()['candles'])

        return Response(status=status.HTTP_200_OK, data=self.serializer_class(result_data, many=True).data)


class ActionOrderBookGetAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ActionOrderBookResponseSerializer

    @extend_schema(
        tags=['Real-time market data - Акции'],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Ошибка при запросе к MOEX API',
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string',
                            'example': 'Ошибка при запросе к MOEX API.'
                        },
                    },
                },
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description='Учетные данные не предоставлены',
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string',
                            'example': 'Authentication credentials were not provided.'
                        },
                    },
                },
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        },
        summary='Получить стакан котировок по одной указанной акции',
        description=(
            f'Возвращает стакан котировок по одной указанной акции, 10 уровней Buy, 10 уровней Sell, '
            f'включая:\n\n{serializer_class.Meta.description}'
        ),
        parameters=[
            OpenApiParameter(
                name='ticker',
                location=OpenApiParameter.PATH,
                description='Код ценной бумаги',
                examples=[
                    OpenApiExample(
                        'Акция Сбербанка',
                        value='SBER',
                    ),
                ],
                type=str,
                required=True,
            ),
        ],
    )
    def get(self, request, ticker, *args, **kwargs):
        response = MOEXAPIService.get_orderbook_for_action(ticker)
        try:
            response.raise_for_status()
        except HTTPError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Ошибка при запросе к MOEX API'})

        result_data = parse_start_structure(response.json()['orderbook'])

        return Response(status=status.HTTP_200_OK, data=self.serializer_class(result_data, many=True).data)


class ActionTradesGetAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ActionTradesResponseSerializer

    @extend_schema(
        tags=['Real-time market data - Акции'],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Ошибка при запросе к MOEX API',
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string',
                            'example': 'Ошибка при запросе к MOEX API.'
                        },
                    },
                },
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description='Учетные данные не предоставлены',
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {
                            'type': 'string',
                            'example': 'Authentication credentials were not provided.'
                        },
                    },
                },
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        },
        summary='Получить все сделки по одной указанной акции за текущий торговый день',
        description=(
            f'Возвращает все сделки по одной указанной акции за текущий торговый день, '
            f'включая:\n\n{serializer_class.Meta.description}'
        ),
        parameters=[
            OpenApiParameter(
                name='ticker',
                location=OpenApiParameter.PATH,
                description='Код ценной бумаги',
                examples=[
                    OpenApiExample(
                        'Акция Сбербанка',
                        value='SBER',
                    ),
                ],
                type=str,
                required=True,
            ),
            OpenApiParameter(
                name='tradeno',
                location=OpenApiParameter.QUERY,
                description='Получить сделки, которые идут начиная с указанного',
                examples=[
                    OpenApiExample(
                        '13112155195',
                        value='13112155195',
                    ),
                ],
                type=int,
            ),
        ],
    )
    def get(self, request, ticker, *args, **kwargs):
        tradeno = request.query_params.get('tradeno')
        response = MOEXAPIService.get_trades_for_action(ticker, tradeno)
        try:
            response.raise_for_status()
        except HTTPError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Ошибка при запросе к MOEX API'})

        result_data = parse_start_structure(response.json()['trades'])

        return Response(status=status.HTTP_200_OK, data=self.serializer_class(result_data, many=True).data)
