from datetime import datetime

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    isTwoFactor = serializers.BooleanField()
    authProvider = serializers.CharField(max_length=255)
    emailVerifiedAt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", input_formats=['iso-8601'])

    def validate_emailVerifiedAt(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    isTwoFactor = serializers.BooleanField()
    emailVerifiedAt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", input_formats=['iso-8601'])

    def validate_emailVerifiedAt(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    authProvider = serializers.CharField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    key = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UpdatePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(max_length=255)
    newPassword = serializers.CharField(max_length=255)


class VerificationKeySerializer(serializers.Serializer):
    email = serializers.EmailField()
    callBackUrl = serializers.URLField()


class VerifyKeySerializer(serializers.Serializer):
    email = serializers.EmailField()
    key = serializers.CharField(max_length=255)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    callBackUrl = serializers.URLField()


class SessionSerializer(serializers.Serializer):
    sessionToken = serializers.CharField(max_length=255)
    refreshToken = serializers.CharField(max_length=255)


class OAuthLoginSerializer(serializers.Serializer):
    originUrl = serializers.URLField()


class UpsertOAuthUserSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255)
    providerUserId = serializers.CharField(max_length=255)
    accessToken = serializers.CharField(max_length=255)
    refreshToken = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    pictureUrl = serializers.URLField()
    email = serializers.EmailField()
