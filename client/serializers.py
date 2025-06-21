from django.contrib.auth.models import User
from rest_framework import serializers

from client.models import UserInformation, Portfolio, PortfolioAsset


class RegisterInputSerializer(serializers.Serializer):
    """Сериализатор входных данных для регистрации"""

    username = serializers.CharField(max_length=50, help_text='Имя пользователя')
    password = serializers.CharField(min_length=8, help_text='Пароль')


class UserInformationInputSerializer(serializers.ModelSerializer):
    """Сериализатор входных данных информации о пользователе"""

    class Meta:
        model = UserInformation
        exclude = ('user', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор данных о пользователе"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserInformationOutputSerializer(serializers.ModelSerializer):
    """Сериализатор данных информации о пользователе"""

    user = UserSerializer()

    class Meta:
        model = UserInformation
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'
        read_only_fields = ('id', 'user')


class PortfolioAssetSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)

    class Meta:
        model = PortfolioAsset
        fields = ['id', 'portfolio', 'asset', 'asset_name', 'quantity', 'added_at']
        read_only_fields = ('id', 'added_at', 'portfolio')
