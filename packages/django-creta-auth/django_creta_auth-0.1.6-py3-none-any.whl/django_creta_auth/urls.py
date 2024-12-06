from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (
    RegisterUserView, LoginUserView, ResetPasswordView, UpdatePasswordView,
    SendVerificationKeyView, VerifyKeyView, FindExistingUserView, SendPasswordResetView,
    VerifyPasswordResetView, ValidateSessionView, RefreshSessionView, LogoutUserView,
    GoogleOAuthLoginView, AppleOAuthLoginView, UpsertOAuthUserView
)

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for credential and session management.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@runners.im"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('credential/register', RegisterUserView.as_view(), name='register-user'),
    path('credential/login', LoginUserView.as_view(), name='login-user'),
    path('credential/reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('credential/update-password', UpdatePasswordView.as_view(), name='update-password'),
    path('validate/send-verification-key', SendVerificationKeyView.as_view(), name='send-verification-key'),
    path('validate/verify-key', VerifyKeyView.as_view(), name='verify-key'),
    path('validate/find-existing-user', FindExistingUserView.as_view(), name='find-existing-user'),
    path('validate/send-password-reset', SendPasswordResetView.as_view(), name='send-password-reset'),
    path('validate/verify-password-reset', VerifyPasswordResetView.as_view(), name='verify-password-reset'),
    path('session/validate', ValidateSessionView.as_view(), name='validate-session'),
    path('session/refresh', RefreshSessionView.as_view(), name='refresh-session'),
    path('session/logout', LogoutUserView.as_view(), name='logout-user'),
    path('oauth/google', GoogleOAuthLoginView.as_view(), name='google-oauth-login'),
    path('oauth/apple', AppleOAuthLoginView.as_view(), name='apple-oauth-login'),
    path('oauth/upsertUser', UpsertOAuthUserView.as_view(), name='upsert-oauth-user'),
]
