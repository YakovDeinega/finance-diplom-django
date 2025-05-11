from django.db import models

from common_utils.mixins import AutoDateMixin
from moex.models import Asset


# Create your models here.
class MLModel(AutoDateMixin):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    version = models.CharField(max_length=6, default='1.0.0', verbose_name='Версия')
    path = models.URLField(verbose_name='URL к модели')
    is_active = models.BooleanField(default=False, verbose_name='Активна')

    class Meta:
        verbose_name = 'Используемая модель нейронной сети'
        verbose_name_plural = 'Используемые модели нейронных сетей'


class Prediction(AutoDateMixin):
    INTERVALS_OF_PREDICTIONS = (
        ('1', '1 мин'),
        ('10', '10 мин'),
        ('60', '1 час'),
        ('24', '1 день'),
    )

    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, verbose_name='Модель нейронной сети')
    asset = models.ForeignKey(Asset, null=True, on_delete=models.SET_NULL, verbose_name='Финансовый актив')
    last_prediction_date = models.DateTimeField(verbose_name='Последняя дата и время из предсказаний')
    interval_of_predictions = models.CharField(
        max_length=2,
        choices=INTERVALS_OF_PREDICTIONS,
        verbose_name='Интервал предсказаний',
    )
    predicted_values = models.JSONField(verbose_name='Предсказанные значения')
    actual_values = models.JSONField(default=dict, verbose_name='Реальные значения')
    metrics = models.JSONField(default=dict, verbose_name='Метрики')

    class Meta:
        unique_together = ['model', 'asset', 'last_prediction_date', 'interval_of_predictions']
        verbose_name = 'Предсказание'
        verbose_name_plural = 'Предсказания'
