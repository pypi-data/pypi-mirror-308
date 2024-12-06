import hashlib

from django.test import TestCase

from .gateway import login_user, validate_session


def hash_password(password):
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature


class GatewayTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_login_and_validate(self):
        # User credentials
        email = "jayden@runners.im"
        password = "qlalfqjsgh1"
        # hashed_password = hash_password(password)
        # print('hashed_password: ', hashed_password)

        # Login the user
        login_response, login_status = login_user(email, password)
        print('login_response: ', login_response)

        # Check if login was successful
        self.assertEqual(login_status, 200, f"Login failed: {login_response}")

        session_token = login_response.get('session', {}).get('sessionToken')
        print('session_token: ', session_token)
        self.assertIsNotNone(session_token, "Login did not return a session token")

        # Validate the session
        validate_response, validate_status = validate_session(session_token)
        print('validate_response: ', validate_response)

        # Check if session validation was successful
        self.assertEqual(validate_status, 200, f"Session validation failed: {validate_response}")
        self.assertTrue(validate_response.get('isValid'), "Session is not valid")
