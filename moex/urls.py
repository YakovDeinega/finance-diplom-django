
from django.urls import path

from machine_learning.views import MLPredictTickerAPIView
from .views import ActionTradeStatisticsGetAPIView, ActionCandlesGetAPIView, ActionOrderBookGetAPIView, \
    ActionTradesGetAPIView

urlpatterns = [
    path('trade_statistics/', ActionTradeStatisticsGetAPIView.as_view(), name='trade_statistics'),
    path('<str:ticker>/candles/', ActionCandlesGetAPIView.as_view(), name='candles'),
    path('<str:ticker>/orderbook/', ActionOrderBookGetAPIView.as_view(), name='orderbook'),
    path('<str:ticker>/trades/', ActionTradesGetAPIView.as_view(), name='trades'),
    path('predict/<str:ticker>/', MLPredictTickerAPIView.as_view(), name='predict'),
]