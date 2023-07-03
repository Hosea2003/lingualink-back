from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from uuid import uuid4
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from mod_user.models import ValidationCode, LinguaUser
from mod_user.serializers import LinguaUserSerializer, ValidateUserSerializer, AuthSerializer
from mod_user.utils import create_code, check_validation_code
from services.gmail import send_email
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


@api_view(["POST"])
def register_user(request: Request):
    user_data = request.data

    user_serializer = LinguaUserSerializer(data=user_data)

    if not user_serializer.is_valid():
        return Response(user_serializer.errors)

    user: LinguaUser = user_serializer.save()
    # send a validation code
    validation = create_code(user)

    send_email("Your validation code", user.email, "Thanks for choosing Lingualink. "
                                                   "Here is your validation code: {}".format(validation.code))

    return Response({"message": "Validation code sent"}, status=status.HTTP_201_CREATED)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1/accounts/google/login/callback/"


@api_view(["POST"])
def validate_account(request: Request):
    data = request.data
    result = check_validation_code(data)

    if not result.get("success"):
        return Response({"message": result.get("message")}, status=result.get("status"))

    user_code = result.get("message")

    user = user_code.user_to_validate
    user.account_verified = True
    user.save()
    user_code.delete()

    return Response({"message": "account validated"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_validation_code(request: Request):
    data = request.data
    username = data.get("username")

    if not username:
        return Response({"message": "Provide an username"}, status=status.HTTP_400_BAD_REQUEST)

    user = LinguaUser.objects.filter(username=username).first()
    if not user:
        return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    validation = create_code(user)
    send_email("Validation code", user.email, "To reset your password, here is your validation code {}"
               .format(validation.code))

    return Response({"message": "validation code sent"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def obtain_token(request: Request):
    data = request.data
    serializer = AuthSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=data.get("username"), password=data.get("password"))

    if not user:
        return Response({"errors": "Unable to log in with provided credentials"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.account_verified:
        return Response({"errors":"Account not verified, enter your validation code"}, status=status.HTTP_403_FORBIDDEN)

    token = Token.objects.create(user=user)

    return Response({"token":token.key})
