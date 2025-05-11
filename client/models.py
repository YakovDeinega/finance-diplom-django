from django.contrib.auth.models import User
from django.db import models

from common_utils.mixins import AutoDateMixin
from moex.models import Asset


# Create your models here.
class UserInformation(AutoDateMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=11, blank=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png', verbose_name='Аватар')
    balance = models.FloatField(default=0, verbose_name='Баланс')
    email_confirmed = models.BooleanField(default=False, verbose_name='Электронная почта подтверждена')

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информации о пользователях'


class Portfolio(AutoDateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Название')
    is_main = models.BooleanField(default=False, verbose_name='Является ли основным')

    class Meta:
        verbose_name = 'Портфель пользователя'
        verbose_name_plural = 'Портфели пользователей'


class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, verbose_name='Портфель')
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, verbose_name='Финансовый актив')
    quantity = models.PositiveIntegerField(verbose_name='Число активов')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        unique_together = ['portfolio', 'asset']
        verbose_name = 'Актив в портфеле'
        verbose_name_plural = 'Активы в портфелях'

