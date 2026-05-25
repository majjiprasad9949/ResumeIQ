from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)

from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    RegisterSerializer
)

User = get_user_model()


class CustomTokenObtainPairSerializer(
    TokenObtainPairSerializer
):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(
            user
        )

        token["email"] = user.email

        return token


class UserViewSet(
    viewsets.GenericViewSet
):

    queryset = User.objects.all()

    serializer_class = UserSerializer


    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny]
    )
    def register(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(

            {
                "message":
                "Registration successful",

                "user":
                UserSerializer(
                    user
                ).data
            },

            status=status.HTTP_201_CREATED
        )


    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny]
    )
    def login(self, request):

        email = request.data.get(
            "email"
        )

        password = request.data.get(
            "password"
        )

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(

                {
                    "detail":
                    "Invalid credentials"
                },

                status=400
            )


        if not user.check_password(
            password
        ):

            return Response(

                {
                    "detail":
                    "Invalid credentials"
                },

                status=400
            )


        token = (
            CustomTokenObtainPairSerializer
            .get_token(
                user
            )
        )


        return Response(

            {
                "access":
                str(token.access_token),

                "refresh":
                str(token),

                "user":
                UserSerializer(
                    user
                ).data
            }

        )


    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):

        return Response(

            UserSerializer(
                request.user
            ).data

        )