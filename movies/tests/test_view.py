import pytest
from authentication.models import CustomUser
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from movies.models import Movie

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

    def test_GetAllMovies(self):
        user1 = mixer.blend(CustomUser, first_name='Prasad')

        url = reverse('get-and-create-movies')
        print("url", url)
        response = self.client.get(url)
        print("response", dir(response))
        print(response.json(), '+++++++++++++')

        assert response.status_code == 403

    def test_CreateNewMovie(self):
        user1 = mixer.blend(CustomUser, first_name='Prasad')

        url = reverse('get-and-create-movies')
        print("url", url)
        data = {'name': 'can_view_data', 'rank': 1}
        response = self.client.post(url, data=data)
        print("response", dir(response))
        print(response.json(), '+++++++++++++')

        assert response.status_code == 201

    def test_CreateNewMovieFail(self):
        user1 = mixer.blend(CustomUser, first_name='Prasad')

        url = reverse('get-and-create-movies')
        print("url", url)
        data = {'name': 'k', }
        response = self.client.post(url, )
        print("response", dir(response))
        assert response.status_code == 400

    def test_movie_not_exists(self):
        url = reverse('update-movie', kwargs={'pk': 12})
        data = {'name': 'k', }
        response = self.client.put(url, data=data)
        assert response.status_code == 404

    def test_UpdateMovie(self):
        user1 = mixer.blend(Movie)

        url = reverse('update-movie', kwargs={'pk': user1.id})
        print("url", url)
        data = {'name': 'k', 'rank': 54}
        response = self.client.put(url, data=data)
        print("response", dir(response))
        print(response.status_code)
        assert response.status_code == 200

    def test_UpdateMovieFail(self):
        user1 = mixer.blend(Movie, )
        user_id = user1.id

        url = reverse('update-movie', kwargs={'pk': user_id})
        print("url", url)
        data = {'name': 'k'}
        response = self.client.put(url, )
        print("response", dir(response))
        assert response.status_code == 400

    def test_deleteAMovie(self):
        user1 = mixer.blend(Movie, )
        url = reverse('delete-movie', kwargs={'pk': user1.id})
        print("url", url)
        response = self.client.delete(url)
        print("response", dir(response))
        assert response.status_code == 204
