from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from client.serializers import RegisterInputSerializer


def hero_view(request):
    return render(request, 'client/hero_section.html')


class RegisterAPIView(APIView):

    serializer_class = RegisterInputSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            User.objects.create_user(**serializer.validated_data)
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
