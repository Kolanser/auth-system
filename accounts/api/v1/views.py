from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.v1.serializers import UserLoginSerializer, UserSerializer
from accounts.utils import generate_jwt

User = get_user_model()


class UserRegistrationApiView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserLoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.filter(is_active=True).get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Неверный email или пароль"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"error": "Неверный email или пароль"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"token": generate_jwt(user)}, status=status.HTTP_200_OK)


class UserLogoutApiView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "Успешный выход из системы"}, status=status.HTTP_200_OK)


class UserProfileApiView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class UserDeleteApiView(DestroyAPIView):
    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
