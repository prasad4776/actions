import pytest
from authentication.models import CustomUser
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestParhamView(TestCase):
    def setUp(self):
        self.client = APIClient()
        print("self.client", self.client)
        from rest_framework.authtoken.models import Token
        self.eg_user = CustomUser.objects.create_user(email='test@parham.in', first_name='Test', last_name='User',
                                                      level='AD',
                                                      password='Test1234')
        self.token = Token.objects.create(user=self.eg_user)
        print(self.token.key, 'Tokennnn Keyyyyyyyyyyyy')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_AllCustomUser(self):
        user1 = mixer.blend(CustomUser, first_name='Prasad')

        url = reverse('detail-list')
        print("url", url)
        response = self.client.get(url)
        # response = self.client.get('/api/auth/user/all')
        print("response", dir(response))
        print(response.json(), '+++++++++++++')

        assert response.status_code == 200
        assert len(response.json()) == 2


class TestParhamViewCustomUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        print("self.client", self.client)
        from rest_framework.authtoken.models import Token
        self.eg_user = CustomUser.objects.create_user(email='test@parham.in', first_name='Test', last_name='User',
                                                      level='AD',
                                                      password='Test1234')
        self.token = Token.objects.create(user=self.eg_user)
        print(self.token.key, 'Tokennnn Keyyyyyyyyyyyy')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_AdminCustomUserGET(self):
        user2 = mixer.blend(CustomUser, level='AD')
        print(user2.id, "user2.id")
        user_id = user2.id
        url = reverse('user-get-update', kwargs={'pk': user_id})
        response = self.client.get(url)
        print(response, "response")
        assert response.status_code == 200

    def test_AdminCustomUserDEL(self):
        user2 = mixer.blend(CustomUser, level='AD')
        print(user2.id, "user2.id")
        user_id = user2.id
        url = reverse('user-get-update', kwargs={'pk': user_id})
        response = self.client.delete(url)
        print(response, "response")
        assert response.status_code == 200

    def test_AdminCustomUserUPD(self):
        user2 = mixer.blend(CustomUser, level='AD')
        print(user2.id, "user2.id")
        user_id = user2.id
        url = reverse('user-get-update', kwargs={'pk': user_id})
        updt_data = {'new_password': 'xyzz123', 'new_groups': '', 'new_level': 'L1'}
        response = self.client.put(url, data=updt_data)
        print(response, "response")
        assert response.status_code == 200
