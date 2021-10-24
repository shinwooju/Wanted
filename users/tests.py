import json
import bcrypt

from django.test import TestCase, Client

from unittest.mock import MagicMock, patch
from .models       import User


class SignUpTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id       = 1,
                    name     = "wooju0",
                    email    = "zkzkxls@naver.com",
                    password = "wooju123!@",
                ),
                User(
                    id       = 2,
                    name     = "wooju1",
                    email    = "zkzkxls@gmail.com",
                    password = "wooju12!@"
                ),
                User(
                    id       = 3,
                    name     = "wooju2",
                    email    = "zkzkxls@hanmail.com",
                    password = "wooju12!@#$!"
                )
            ]
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_view_create_success(self):
        user = {
            "name"           : "wooju3",
            "email"          : "zkzkxls123@naver.com",
            "password"       : "wooju111!@",
            "check_password" : "wooju111!@"
        }

        client   = Client()
        response = client.post(
            "/users/sign-up", json.dumps(user), content_type = "application/json"
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE" : "SUCCESS"})

    def test_signup_view_empty_value(self):
        user = {
            "name"           : "",
            "email"          : "zkzkxlsnaver.com",
            "password"       : "wooju1212!@",
            "check_password" : "wooju1212!@"
        }

        client   = Client()
        response = client.post(
            "/users/sign-up", json.dumps(user), content_type = "application/json"
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "EMPTY_VALUE"})

    def test_siguup_view_invalid_email(self):
        user = {
            "name"           : "wooju4",
            "email"          : "zkzkxlsnaver.com",
            "password"       : "wooju1212!@",
            "check_password" : "wooju1212!@"
        }

        client   = Client()
        response = client.post(
            "/users/sign-up", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "EMAIL_VALIDATION"})

    def test_signup_view_invalid_password(self):
        user = {
            "name"           : "wooju5",
            "email"          : "zkzkxls1234@naver.com",
            "password"       : "wooju1212",
            "check_password" : "wooju1212!@"
        }

        client   = Client()
        response = client.post(
            "/users/sign-up", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "PASSWORD_VALIDATION"})

    def test_signup_view_exist_email(self):
        user = {
            "name"           : "wooju7",
            "email"          : "zkzkxls@naver.com",
            "password"       : "wooju1212!@",
            "check_password" : "wooju1212!@"
        }

        client   = Client()
        response = client.post(
            "/users/sign-up", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "ALREADY_EXISTED_EAMIL"})

    def test_signup_view_check_password(self):
        user = {
            "name"           : "wooju10",
            "email"          : "zkzkxls77@naver.com",
            "password"       : "wooju1212!@",
            "check_password" : "wooju1212"
        }

        client   = Client()
        response = client.post(
            "/users/sign-up", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "PASSWORD_NOT_CORRECT"})

    def test_signup_view_key_error(self):
        user = {
            "na"             : "grg",
            "email"          : "zkzkxls@na.com",
            "password"       : "wooju1212!@",
            "check_password" : "wooju1212!@"
        }

        client   = Client()
        response = client.post(
            "/users/sign-up", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "KEY_ERROR"})

class SignInTest(TestCase):
    def setUp(self):
        password = "wooju123!!"
        hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(
                    id       = 1,
                    name     = "wooju",
                    email    = "zkzkxls@abc.com",
                    password = hashed_password
                )

    def tearDown(self):
        User.objects.all().delete()

    @patch("requests.post")
    def test_signin_view_success(self, mocked_requests):
        user = {
            "email"    : "zkzkxls@abc.com",
            "password" : "wooju123!!",
        }

        class MockedResponse:
            def json(self):
                return {    
                    "MESSAGE" : "SUCCESS",
                    'TOKEN'   :  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.-_VJaTCP79-P4plBBkOt-TpaaVCkQeHHgSNmozV6auc"
                }

        client   = Client()
        mocked_requests.post = MagicMock(return_value = MockedResponse())

        response = client.post(
            "/users/sign-in", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 201)
        
    def test_signin_view_empty_value(self):
        user = {
            "email"    : "",
            "password" : "wooju123!!",
        }

        client   = Client()
        response = client.post(
            "/users/sign-in", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "EMPTY_VALUE"})

    def test_signin_view_not_exist_user(self):
        user = {
            "email"    : "zkzkxls@naver.com",
            "password" : "wooju123!!",
        }

        client   = Client()
        response = client.post(
            "/users/sign-in", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE" : "USER_DOES_NOT_EXIST"})

    def test_signin_view_invalid_password(self):
        user = {
            "email"    : "zkzkxls@abc.com",
            "password" : "wooju123@",
        }

        client   = Client()
        response = client.post(
            "/users/sign-in", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE" : "INVALID_PASSWORD"})

    def test_signin_view_key_error(self):
        user = {
            "ema"      : "zkzkxls@abc.com",
            "password" : "wooju123@",
        }

        client   = Client()
        response = client.post(
            "/users/sign-in", json.dumps(user), content_type = "application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "KEY_ERROR"})