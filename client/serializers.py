from rest_framework import serializers


class RegisterInputSerializer(serializers.Serializer):
    """Сериализатор входных данных для регистрации"""

    username = serializers.CharField(max_length=50, help_text='Имя пользователя')
    password = serializers.CharField(min_length=8, help_text='Пароль')
