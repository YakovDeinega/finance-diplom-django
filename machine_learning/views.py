import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiExample
from requests import HTTPError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from machine_learning.models import Prediction, MLModel
from machine_learning.serializers import PredictActionCandlesResponseSerializer
from moex.create_functions import parse_start_structure, set_appropriate_datetime
from moex.models import Asset
from services.ml_fastapi import MLAPIService
from services.moex import MOEXAPIService


# Create your views here.
class MLPredictTickerAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PredictActionCandlesResponseSerializer

    @extend_schema(
        tags=['Прогнозирование котировок акций'],
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
        summary='Предсказать цены закрытия свечей на следующие 20 рабочих часов Московской Биржи',
        description=(
            f'Возвращает предсказанные цены закрытия свечей по одной указанной акции на следующие 20 рабочих часов'
            f'Московской Биржи, включая:\n\n{serializer_class.Meta.description}'
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
    @method_decorator(cache_page(60 * 15))
    def get(self, request, ticker, *args, **kwargs):
        date_today = datetime.date.today()
        interval = 60
        response_from_moex = MOEXAPIService.get_candles_for_action(
            ticker=ticker,
            dt_from=str(date_today-datetime.timedelta(days=7)),
            dt_till=str(date_today+datetime.timedelta(days=-3)),
            interval=interval,
        )
        try:
            response_from_moex.raise_for_status()
        except HTTPError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Ошибка при запросе к MOEX API'})

        response_data = response_from_moex.json()['candles']
        parsed_data_from_moex = parse_start_structure(response_data)
        if datetime.datetime.strptime(parsed_data_from_moex[-1]['end'], '%Y-%m-%d %H:%M:%S').time().minute > 30:
            start_index, end_index, predict_starting_with_next_hour = -21, None, True
        else:
            start_index, end_index, predict_starting_with_next_hour = -22, -1, False
        parsed_data_from_moex = parsed_data_from_moex[start_index:end_index]

        last_date_end = parsed_data_from_moex[-1]['end']
        request_data_to_ml = {'last_date_end': last_date_end, 'data': [data['close'] for data in parsed_data_from_moex]}

        response_from_ml = MLAPIService.predict(ticker, request_data_to_ml)
        try:
            response_from_ml.raise_for_status()
        except HTTPError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Ошибка при запросе к ML API'})

        result_data = set_appropriate_datetime(response_from_ml.json(), last_date_end, predict_starting_with_next_hour)
        Prediction.objects.create(
            model=MLModel.objects.get(id=1),
            asset=Asset.objects.get(ticker=ticker),
            last_prediction_date=last_date_end,
            interval_of_predictions=interval,
            predicted_values=result_data,
        )
        return Response(status=status.HTTP_200_OK, data=self.serializer_class(result_data, many=True).data)
