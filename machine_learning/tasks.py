import datetime
import logging

from celery import shared_task
from django.utils import timezone

from moex.create_functions import parse_start_structure
from services.moex import MOEXAPIService
from .models import Prediction
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logger = logging.getLogger(__name__)

@shared_task
def update_all_predictions_metrics():
    """Задача для ежедневного обновления метрик всех предсказаний"""
    predictions = Prediction.objects.filter(
        actual_values={},
        metrics={},
        last_prediction_date__lt=datetime.datetime.today()-datetime.timedelta(days=2),
    ).select_related('asset')
    predictions_to_be_updated = []

    for prediction in predictions:
        try:
            # 1. Получаем предсказанные значения
            predicted_data = prediction.predicted_values

            # 2. Определяем временной диапазон для запроса актуальных данных
            begin_dates = [datetime.datetime.strptime(item['begin'], '%Y-%m-%d %H:%M:%S') for item in predicted_data]
            end_dates = [datetime.datetime.strptime(item['end'], '%Y-%m-%d %H:%M:%S') for item in predicted_data]

            min_date = min(begin_dates)
            max_date = max(end_dates)

            info_from_moex = MOEXAPIService.get_candles_for_action(
                ticker=prediction.asset.ticker,
                dt_from=min_date.strftime('%Y-%m-%d'),
                dt_till=max_date.strftime('%Y-%m-%d'),
                interval=prediction.interval_of_predictions,
            ).json()

            actual_candles = parse_start_structure(info_from_moex['candles'])

            # 4. Сопоставляем данные и вычисляем метрики
            y_pred = []
            y_true = []

            for pred_item in predicted_data:
                # Находим соответствующую актуальную свечу
                actual_item = next(
                    (
                        item for item in actual_candles
                        if item['begin'] == pred_item['begin'] and item['end'] == pred_item['end']
                    ),
                    None,
                )

                if actual_item:
                    y_pred.append(pred_item['close'])
                    y_true.append(actual_item['close'])

            # Если нет совпадающих данных, пропускаем
            if not y_true:
                continue

            # 5. Вычисляем метрики
            metrics = {
                'mae': float(mean_absolute_error(y_true, y_pred)),
                'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
                'r2': float(r2_score(y_true, y_pred)),
                'samples': len(y_true),  # Количество успешно сопоставленных точек
                'last_updated': timezone.now().isoformat(),
            }

            # 6. Сохраняем актуальные значения и метрики
            actual_values = [
                {'end': value['end'], 'begin': value['begin'], 'close': value['close']}
                for value in actual_candles
            ]
            prediction.actual_values = actual_values  # Сохраняем полученные данные
            prediction.metrics = metrics
            predictions_to_be_updated.append(prediction)

        except Exception as e:
            logger.info(f"Error updating prediction {prediction.id}: {str(e)}")

    Prediction.objects.bulk_update(predictions_to_be_updated, fields=['actual_values', 'metrics'])
