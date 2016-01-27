from django.core.urlresolvers import reverse
from rest_framework import status
from faker import Factory
from v1.models import User
from v1.tests.base import BaseTest


fake = Factory.create()


class TestUsersView(BaseTest):

    def test_should_successfully_create_a_user(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/users/'
        data = {
            'username': fake.first_name(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': fake.password()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertTrue(response.data['id'] is not None)
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertEqual(response.data['username'], data['username'])
        with self.assertRaises(KeyError):
            response.data['results']['password']
            response.data['results']['activation_token']
            response.data['results']['password_token']

    def test_reject_a_user_with_a_malformed_email_address(self):
        """
        Ensure that we do not accept bad emails.
        """
        url = '/api/v1/users/'
        data = {
            'username': fake.first_name(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': 'trevor',
            'password': fake.password()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['email'] is not None)

    def test_reject_a_user_with_a_blank_password(self):
        """
        Ensure that we do not accept blank passwords.
        """
        url = '/api/v1/users/'
        data = {
            'username': fake.first_name(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['password'] is not None)

    def test_reject_a_user_with_a_blank_username(self):
        """
        Ensure that we do not accept blank usernames.
        """
        url = '/api/v1/users/'
        data = {
            'username': '',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': fake.password()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['username'] is not None)

    def test_successfully_get_a_users_token(self):
        """
        Ensure that we can get a token for the user
        """
        url = reverse('oauth2_provider:token')
        auth_headers = self.get_basic_auth_header(
            self.application.client_id, self.application.client_secret)
        data = {
            'grant_type': 'password',
            'username': 'test_user',
            'password': '123456',
        }
        # The user is not active yet, so we have to manually set it.
        self.test_user.is_active = True
        self.test_user.save()
        response = self.client.post(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successfully_revoke_a_users_token(self):
        """
        Ensure that we can revoke a token for the user
        """
        url = reverse('oauth2_provider:revoke-token')
        data = {
            'client_id': self.application.client_id,
            'client_secret': self.application.client_secret,
            'token': self.access_token.token,
        }
        # The user is not active yet, so we have to manually set it.
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successfully_get_a_users_information(self):
        """
        Ensure that the user can GET himself.
        """
        url = '/api/v1/users/self/'
        auth_headers = self.get_access_token_header()
        response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.test_user.email)
        self.assertEqual(response.data['first_name'],
                         self.test_user.first_name)
        self.assertTrue(response.data['id'] is not None)
        self.assertEqual(response.data['last_name'], self.test_user.last_name)
        self.assertEqual(response.data['username'], self.test_user.username)
        with self.assertRaises(KeyError):
            response.data['results']['password']
            response.data['results']['activation_token']
            response.data['results']['password_token']

    def test_rejecting_get_a_users_information_with_invalid_token(self):
        """
        Ensure that the user cannot GET himself without a token.
        """
        url = '/api/v1/users/self/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successfully_get_all_users_information(self):
        """
        Ensure that the user can GET all other users.
        """
        url = '/api/v1/users/'
        auth_headers = self.get_access_token_header()
        response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertTrue(response.data['results'] is not None)
        self.assertEqual(len(response.data['results']), 2)
        with self.assertRaises(KeyError):
            response.data['results'][0]['email']
            response.data['results'][0]['password']
            response.data['results'][0]['activation_token']
            response.data['results'][0]['password_token']

    def test_rejecting_get_all_users_information_with_invalid_token(self):
        """
        Ensure that the user cannot GET all other users without a token.
        """
        url = '/api/v1/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successfully_get_a_specific_users_information(self):
        """
        Ensure that the user can GET another user.
        """
        url = '/api/v1/users/1/'
        auth_headers = self.get_access_token_header()
        response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'],
                         self.test_user.first_name)
        self.assertEqual(response.data['last_name'], self.test_user.last_name)
        self.assertEqual(response.data['username'], self.test_user.username)
        with self.assertRaises(KeyError):
            response.data['results']['email']
            response.data['results']['password']
            response.data['results']['activation_token']
            response.data['results']['password_token']

    def test_rejecting_get_a_specific_user_with_invalid_token(self):
        """
        Ensure that the user cannot GET another user without a valid token.
        """
        url = '/api/v1/users/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successfully_updating_a_users_information(self):
        """
        Ensure that the user can PUT himself.
        """
        before_test_user = User.objects.get(pk=self.test_user.id)
        url = '/api/v1/users/self/'
        auth_headers = self.get_access_token_header()
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': fake.password(),
            'username': fake.first_name(),
            'bio': 'new bio here yo'
        }
        response = self.client.put(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        after_test_user = User.objects.get(pk=self.test_user.id)
        self.assertEqual(after_test_user.email, data['email'])
        self.assertEqual(after_test_user.first_name, data['first_name'])
        self.assertTrue(after_test_user.id is not None)
        self.assertEqual(after_test_user.last_name, data['last_name'])
        self.assertNotEqual(before_test_user.password,
                            after_test_user.password)
        self.assertNotEqual(after_test_user.password, data['password'])
        self.assertEqual(after_test_user.bio, data['bio'])
        self.assertEqual(after_test_user.username, data['username'])

    def test_successfully_updating_a_users_field(self):
        """
        Ensure that the user can PUT himself.
        """
        before_test_user = User.objects.get(pk=self.test_user.id)
        url = '/api/v1/users/self/'
        auth_headers = self.get_access_token_header()
        data = {
            'email': fake.email(),
        }
        response = self.client.put(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        after_test_user = User.objects.get(pk=self.test_user.id)
        self.assertEqual(after_test_user.email, data['email'])

    def test_rejecting_updating_a_blank_username_information(self):
        """
        Ensure that the user cannot PUT himself with a blank username.
        """
        before_test_user = User.objects.get(pk=self.test_user.id)
        url = '/api/v1/users/self/'
        auth_headers = self.get_access_token_header()
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': fake.password(),
            'username': ''
        }
        response = self.client.put(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after_test_user = User.objects.get(pk=self.test_user.id)
        self.assertEqual(after_test_user, before_test_user)

    def test_rejecting_updating_an_invalid_email_users_information(self):
        """
        Ensure that the user cannot PUT himself with an invalid email.
        """
        before_test_user = User.objects.get(pk=self.test_user.id)
        url = '/api/v1/users/self/'
        auth_headers = self.get_access_token_header()
        data = {
            'email': 'trevor',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': fake.password(),
            'username': fake.first_name()
        }
        response = self.client.put(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after_test_user = User.objects.get(pk=self.test_user.id)
        self.assertEqual(after_test_user, before_test_user)

    def test_rejecting_updating_a_invalid_password_users_information(self):
        """
        Ensure that the user cannot PUT himself with an invalid password.
        """
        before_test_user = User.objects.get(pk=self.test_user.id)
        url = '/api/v1/users/self/'
        auth_headers = self.get_access_token_header()
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': '',
            'username': fake.first_name()
        }
        response = self.client.put(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after_test_user = User.objects.get(pk=self.test_user.id)
        self.assertEqual(after_test_user, before_test_user)

    def test_successfully_activating_a_user(self):
        url = '/api/v1/users/activate/'
        user = User.objects.get(pk=self.test_user.id)
        self.assertFalse(user.is_active)
        data = {
            'activation_token': user.activation_token,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        after_test_user = User.objects.get(pk=self.test_user.id)
        self.assertTrue(after_test_user.is_active)

    def test_successfully_reseting_a_forgotten_password(self):
        url = '/api/v1/users/reset/'
        data = {
            'email': self.test_user.email
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.test_user = User.objects.get(pk=self.test_user.id)
        self.assertTrue(self.test_user.password_token is not None)

    def test_successfully_setting_a_forgotten_password(self):
        url = '/api/v1/users/reset/'
        data = {
            'email': self.test_user.email,
            'password_token': self.test_user.password_token,
            'password': fake.password()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        previous_password = self.test_user.password
        self.test_user = User.objects.get(pk=self.test_user.id)
        self.assertTrue(self.test_user.password is not None)
        self.assertTrue(self.test_user.password != previous_password)
