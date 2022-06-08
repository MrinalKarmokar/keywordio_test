
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import MyUserLoginSerializer, MyUserSignupSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        serializer = MyUserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            res = {
                'msg': 'User Signed Up Successfully',
                'token': token,
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        serializer = MyUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            token = get_tokens_for_user(user)

            if user is not None:
                res = {
                    'msg': 'User Logged In Successfully',
                    'token': token,
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                res = {
                    'non_field_errors': ['User Credentials not valid']
                }
                return Response(res, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------
