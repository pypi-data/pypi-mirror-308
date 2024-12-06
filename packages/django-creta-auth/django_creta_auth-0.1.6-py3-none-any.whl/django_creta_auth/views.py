import requests
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterUserSerializer, LoginUserSerializer, ResetPasswordSerializer,
    UpdatePasswordSerializer, VerificationKeySerializer, VerifyKeySerializer,
    EmailSerializer, PasswordResetSerializer, SessionSerializer, OAuthLoginSerializer,
    UpsertOAuthUserSerializer
)

CRETA_AUTH_BASE_URL = settings.CRETA_AUTH_BASE_URL


class RegisterUserView(APIView):
    @swagger_auto_schema(
        request_body=RegisterUserSerializer,
        responses={
            200: openapi.Response('Existing user', RegisterUserSerializer),
            201: openapi.Response('User created', RegisterUserSerializer),
            400: 'Invalid request',
            500: 'Server error'
        }
    )
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            response = requests.post(f"{CRETA_AUTH_BASE_URL}/credential/register", json=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    @swagger_auto_schema(
        request_body=LoginUserSerializer,
        responses={
            200: openapi.Response('Login successful', LoginUserSerializer),
            400: 'Bad request',
            500: 'Internal server error'
        }
    )
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            response = requests.post(f"{CRETA_AUTH_BASE_URL}/credential/login", json=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={
            200: openapi.Response('Password reset successfully'),
            400: 'Invalid request',
            500: 'Internal server error'
        }
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            response = requests.post(f"{CRETA_AUTH_BASE_URL}/credential/reset-password", json=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    @swagger_auto_schema(
        request_body=UpdatePasswordSerializer,
        responses={
            200: openapi.Response('Password updated successfully'),
            400: 'Invalid request',
            500: 'Internal server error'
        },
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer sessionToken",
                                             type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            headers = {'Authorization': f"Bearer {request.headers.get('Authorization')}"}
            response = requests.post(f"{CRETA_AUTH_BASE_URL}/credential/update-password",
                                     json=serializer.validated_data,
                                     headers=headers)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationKeyView(APIView):
    @swagger_auto_schema(
        request_body=VerificationKeySerializer,
        responses={
            200: openapi.Response('Email verification sent'),
            400: 'Invalid request',
            500: 'Internal server error'
        }
    )
    def post(self, request):
        serializer = VerificationKeySerializer(data=request.data)
        if serializer.is_valid():
            response = requests.post(f"{CRETA_AUTH_BASE_URL}/validate/send-verification-key",
                                     json=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyKeyView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_QUERY, description="Email", type=openapi.TYPE_STRING),
            openapi.Parameter('key', openapi.IN_QUERY, description="Verification key", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('Email verified'),
            400: 'Invalid request',
            401: 'Unauthorized',
            500: 'Internal server error'
        }
    )
    def get(self, request):
        serializer = VerifyKeySerializer(data=request.query_params)
        if serializer.is_valid():
            response = requests.get(f"{CRETA_AUTH_BASE_URL}/validate/verify-key", params=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FindExistingUserView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_QUERY, description="Email", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('User found', EmailSerializer),
            400: 'Invalid request'
        }
    )
    def get(self, request):
        serializer = EmailSerializer(data=request.query_params)
        if serializer.is_valid():
            response = requests.get(f"{CRETA_AUTH_BASE_URL}/validate/find-existing-user",
                                    params=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetView(APIView):
    @swagger_auto_schema(
        request_body=PasswordResetSerializer,
        responses={
            200: openapi.Response('Password reset sent'),
            400: 'Invalid request',
            500: 'Internal server error'
        }
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            response = requests.post(f"{CRETA_AUTH_BASE_URL}/validate/send-password-reset",
                                     json=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPasswordResetView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_QUERY, description="Email", type=openapi.TYPE_STRING),
            openapi.Parameter('key', openapi.IN_QUERY, description="Reset key", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('Password reset verified'),
            400: 'Invalid request',
            500: 'Internal server error'
        }
    )
    def get(self, request):
        serializer = VerifyKeySerializer(data=request.query_params)
        if serializer.is_valid():
            response = requests.get(f"{CRETA_AUTH_BASE_URL}/validate/verify-password-reset",
                                    params=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateSessionView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer sessionToken",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('Session valid'),
            401: 'Invalid session',
            500: 'Internal server error'
        }
    )
    def get(self, request):
        headers = {'Authorization': f"Bearer {request.headers.get('Authorization')}"}
        response = requests.get(f"{CRETA_AUTH_BASE_URL}/session/validate", headers=headers)
        return Response(response.json(), status=response.status_code)


class RefreshSessionView(APIView):
    @swagger_auto_schema(
        request_body=SessionSerializer,
        responses={
            200: openapi.Response('Session refreshed', SessionSerializer),
            400: 'Invalid request',
            401: 'Invalid refresh token',
            500: 'Internal server error'
        }
    )
    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            response = requests.post(f"{CRETA_AUTH_BASE_URL}/session/refresh", json=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer sessionToken",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('User logged out'),
            400: 'Invalid request'
        }
    )
    def post(self, request):
        headers = {'Authorization': f"Bearer {request.headers.get('Authorization')}"}
        response = requests.post(f"{CRETA_AUTH_BASE_URL}/session/logout", headers=headers)
        return Response(response.json(), status=response.status_code)


class GoogleOAuthLoginView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('originUrl', openapi.IN_QUERY, description="The URL to redirect to after login",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('Login successful'),
            400: 'Invalid Google ID token',
            500: 'Internal server error'
        }
    )
    def get(self, request):
        serializer = OAuthLoginSerializer(data=request.query_params)
        if serializer.is_valid():
            response = requests.get(f"{CRETA_AUTH_BASE_URL}/oauth/google", params=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppleOAuthLoginView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('originUrl', openapi.IN_QUERY, description="The URL to redirect to after login",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('Login successful'),
            400: 'Invalid token',
            500: 'Internal server error'
        }
    )
    def get(self, request):
        serializer = OAuthLoginSerializer(data=request.query_params)
        if serializer.is_valid():
            response = requests.get(f"{CRETA_AUTH_BASE_URL}/oauth/apple", params=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpsertOAuthUserView(APIView):
    @swagger_auto_schema(
        request_body=UpsertOAuthUserSerializer,
        responses={
            200: openapi.Response('Login successful', UpsertOAuthUserSerializer),
            400: 'Invalid OAuth provider',
            500: 'Failed to update OAuth account'
        }
    )
    def post(self, request):
        serializer = UpsertOAuthUserSerializer(data=request.data)
        if serializer.is_valid():
            response = requests.post(f"{CRETA_AUTH_BASE_URL}/oauth/upsertUser", json=serializer.validated_data)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
