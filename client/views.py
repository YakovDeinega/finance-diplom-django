from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.

from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from client.models import UserInformation, Portfolio, PortfolioAsset
from client.serializers import RegisterInputSerializer, UserInformationInputSerializer, UserInformationOutputSerializer, \
    PortfolioSerializer, PortfolioAssetSerializer


def hero_view(request):
    return render(request, 'client/hero_section.html')


class RegisterAPIView(APIView):

    serializer_class = RegisterInputSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**serializer.validated_data)
            UserInformation.objects.create(user=user)
            return Response(
                {
                    'status': 'success',
                    'message': 'Регистрация успешна!'
                },
                status=status.HTTP_201_CREATED
            )
        except Exception:
            return Response(
                {
                    'status': 'error',
                    'message': 'Ошибка регистрации'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class GetOrUpdateUserInformationAPIView(APIView):

    permission_classes = [IsAuthenticated]
    input_serializer_class = UserInformationInputSerializer
    output_serializer_class = UserInformationOutputSerializer

    @extend_schema(
        description='Добавьте информацию о пользователе',
        request=UserInformationInputSerializer,
    )
    def post(self, request):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserInformation.objects.filter(user=request.user).update(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        description='Получите информацию о пользователе',
    )
    def get(self, request):
        user_information = get_object_or_404(UserInformation, user=request.user)
        return Response(status=status.HTTP_200_OK, data=self.output_serializer_class(user_information).data)


class PortfolioAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    @extend_schema(
        description='Получить портфели пользователя',
    )
    def get(self, request):
        portfolios = Portfolio.objects.filter(user=request.user)
        return Response(self.serializer_class(portfolios, many=True).data)

    @extend_schema(
        description='Обновить портфели пользователя'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PortfolioAssetAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioAssetSerializer

    @extend_schema(
        description='Получить активы пользователя',
    )
    def get(self, request, portfolio_id):
        assets = PortfolioAsset.objects.filter(portfolio__user=request.user, portfolio_id=portfolio_id)
        return Response(self.serializer_class(assets, many=True).data)

    @extend_schema(
        description='Обновить активы пользователя'
    )
    def post(self, request, portfolio_id):
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        asset_id = request.data.get('asset')
        existing_asset = PortfolioAsset.objects.filter(portfolio=portfolio, asset_id=asset_id).first()

        if existing_asset:
            serializer = self.serializer_class(existing_asset, data=request.data, partial=True)
        else:
            serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(portfolio=portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)
