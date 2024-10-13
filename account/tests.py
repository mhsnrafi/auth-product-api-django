from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User


class AccountTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'name': 'Test User',
            'tc': True
        }
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User',
            tc=True
        )
    def test_user_login(self):
        url = reverse('login')
        data = {'email': 'testuser@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_profile_access_authenticated(self):
        self.client.login(email='testuser@example.com', password='testpass123')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_request(self):
        url = reverse('send-reset-password-email')
        data = {'email': 'testuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)