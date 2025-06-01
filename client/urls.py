from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from client import views
from client.views import RegisterAPIView

urlpatterns = [
    path('', views.hero_view, name='home'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]