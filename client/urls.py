from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from client import views
from client.views import RegisterAPIView, GetOrUpdateUserInformationAPIView, PortfolioAPIView, PortfolioAssetAPIView

urlpatterns = [
    path('', views.hero_view, name='home'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('user_information/', GetOrUpdateUserInformationAPIView.as_view(), name='user_information'),
    path('portfolios/', PortfolioAPIView.as_view(), name='portfolio-list'),
    path('portfolios/<int:portfolio_id>/assets/', PortfolioAssetAPIView.as_view(), name='portfolio-assets'),
]