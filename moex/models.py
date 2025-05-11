from django.db import models

from common_utils.mixins import AutoDateMixin


# Create your models here.
class Asset(AutoDateMixin):
    ticker = models.CharField(max_length=10, unique=True, verbose_name='Уникальный идентификатор финансового актива')
    isin = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='Международный идентификационный код ценной бумаги',
    )
    name = models.CharField(max_length=300, verbose_name='Название')
    registry_number = models.CharField(max_length=50, blank=True, verbose_name='Регистрационный номер')
    nominal = models.DecimalField(max_digits=15, decimal_places=4, null=True, verbose_name='Номинал')
    currency = models.CharField(max_length=20, blank=True, verbose_name='Валюта')
    emitent_inn = models.CharField(max_length=12, blank=True, verbose_name='ИНН эмитента')
    emitent_name = models.CharField(max_length=300, blank=True, verbose_name='Эмитент')
    list_section = models.CharField(max_length=50, blank=True, verbose_name='Секция листинга')
    registry_date = models.DateField(null=True, blank=True, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return f'{self.ticker} ({self.name})'
