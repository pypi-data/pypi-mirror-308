import requests
from django.conf import settings

CRETA_AUTH_BASE_URL = settings.CRETA_AUTH_BASE_URL
CRETA_AUTH_TOKEN = settings.CRETA_AUTH_TOKEN


def get_headers(x_auth_token=None, use_authorization=True):
    headers = {'Content-Type': 'application/json'}
    if x_auth_token:
        headers['x-auth-token'] = f"Bearer {x_auth_token}"
    if use_authorization:
        headers['Authorization'] = f"Bearer {CRETA_AUTH_TOKEN}"
    print(headers)
    return headers


def handle_response(response):
    if response.status_code == 200 or response.status_code == 201:
        return response.json(), response.status_code
    else:
        return {
            "error": response.json().get("error", "Unknown error"),
            "message": response.json().get("message", "An error occurred"),
            "status_code": response.status_code
        }, response.status_code


# Register user
def register_user(email, password, name, is_two_factor, email_verified_at, callback_url=None):
    url = f"{CRETA_AUTH_BASE_URL}/auth/register"
    payload = {
        "user": {
            "email": email,
            "password": password,
            "name": name,
            "isTwoFactor": is_two_factor,
            "emailVerifiedAt": email_verified_at,
        },
        "callbackUrl": callback_url
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return handle_response(response)


# Login user
def login_user(email, password):
    url = f"{CRETA_AUTH_BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return handle_response(response)


# Reset password
def reset_password(email, key, password):
    url = f"{CRETA_AUTH_BASE_URL}/auth/reset-password"
    payload = {
        "email": email,
        "key": key,
        "password": password
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return handle_response(response)


# Update password
def update_password(old_password, new_password):
    url = f"{CRETA_AUTH_BASE_URL}/auth/update-password"
    payload = {
        "oldPassword": old_password,
        "newPassword": new_password
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return handle_response(response)


# Send verification key
def send_verification_key(email, call_back_url):
    url = f"{CRETA_AUTH_BASE_URL}/auth/send-verification-key"
    payload = {
        "email": email,
        "callBackUrl": call_back_url
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return handle_response(response)


# Verify key
def verify_key(email, key):
    url = f"{CRETA_AUTH_BASE_URL}/auth/verify-key"
    params = {
        "email": email,
        "key": key
    }
    response = requests.get(url, params=params, headers=get_headers())
    return handle_response(response)


# Find existing user
def find_existing_user(email):
    url = f"{CRETA_AUTH_BASE_URL}/auth/user-exist"
    params = {"email": email}
    response = requests.get(url, params=params, headers=get_headers())
    return handle_response(response)


# Send password reset
def send_password_reset(email, call_back_url):
    url = f"{CRETA_AUTH_BASE_URL}/auth/send-password-reset"
    payload = {
        "email": email,
        "callBackUrl": call_back_url
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return handle_response(response)


# Verify password reset
def verify_password_reset(email, key):
    url = f"{CRETA_AUTH_BASE_URL}/auth/verify-password-reset"
    params = {
        "email": email,
        "key": key
    }
    response = requests.get(url, params=params, headers=get_headers())
    return handle_response(response)


# Validate session (x_auth_token passed as a parameter)
def validate_session(x_auth_token):
    url = f"{CRETA_AUTH_BASE_URL}/auth/validate-session"
    response = requests.post(url, headers=get_headers(x_auth_token=x_auth_token, use_authorization=True))
    return handle_response(response)


# Refresh session
def refresh_session(refresh_token):
    url = f"{CRETA_AUTH_BASE_URL}/auth/refresh-session"
    payload = {"refreshToken": refresh_token}
    response = requests.post(url, json=payload, headers=get_headers())
    return handle_response(response)


# Logout user
def logout_user():
    url = f"{CRETA_AUTH_BASE_URL}/auth/logout"
    response = requests.post(url, headers=get_headers(use_authorization=True))
    return handle_response(response)


# Google OAuth login
def google_oauth_login(origin_url):
    url = f"{CRETA_AUTH_BASE_URL}/auth/google"
    params = {"originUrl": origin_url}
    response = requests.get(url, params=params, headers=get_headers())
    return handle_response(response)


# Apple OAuth login
def apple_oauth_login(origin_url):
    url = f"{CRETA_AUTH_BASE_URL}/auth/apple"
    params = {"originUrl": origin_url}
    response = requests.get(url, params=params, headers=get_headers())
    return handle_response(response)


# Upsert OAuth user
def upsert_oauth_user(provider, provider_user_id, access_token, refresh_token, name, picture_url, email):
    url = f"{CRETA_AUTH_BASE_URL}/auth/upsert"
    payload = {
        "provider": provider,
        "providerUserId": provider_user_id,
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "name": name,
        "pictureUrl": picture_url,
        "email": email
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return handle_response(response)
