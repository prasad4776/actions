import pytest
from authentication.models import CustomUser
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from roles.models import Role

pytestmark = pytest.mark.django_db


class TestRolesView(TestCase):
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

    def test_GetAllRoles(self):
        user1 = mixer.blend(CustomUser, first_name='Prasad')

        url = reverse('get')
        print("url", url)
        response = self.client.get(url)
        print("response", dir(response))
        print(response.json(), '+++++++++++++')

        assert response.status_code == 200

    def test_role_not_exists(self):
        url = reverse('update-role', kwargs={'pk': 12})
        data = {'name': 'k', 'module': 'Movie', 'kind': 'View', 'priority': '4',
                'filters': '{"name__startswith":"m"}'}
        response = self.client.put(url, data=data)
        assert response.status_code == 404

    def test_CreateNewRole(self):
        user1 = mixer.blend(CustomUser, first_name='Prasad')

        url = reverse('get')
        print("url", url)
        data = {'name': 'can_view_data', 'module': 'Movie', 'kind': 'View', 'priority': '4',
                'filters': '{"name__startswith":"m"}'}
        response = self.client.post(url, data=data)
        print("response", dir(response))
        print(response.json(), '+++++++++++++')

        assert response.status_code == 201

    def test_CreateNewRoleFail(self):
        user1 = mixer.blend(CustomUser, first_name='Prasad')

        url = reverse('get')
        print("url", url)
        data = {'name': 'k', 'module': 'Movie', 'kind': 'View', 'priority': '4',
                'filters': '{"name__startswith":"m"}'}
        response = self.client.post(url, )
        print("response", dir(response))
        assert response.status_code == 400

    def test_UpdateRole(self):
        user1 = mixer.blend(Role, filters={'nam': 'l'})

        url = reverse('update-role', kwargs={'pk': user1.id})
        print("url", url)
        data = {'name': 'k', 'module': 'Movie', 'kind': 'View', 'priority': '4',
                'filters': '{"name__startswith":"m"}'}
        response = self.client.put(url, data=data)
        print("response", dir(response))
        print(response.status_code)
        assert response.status_code == 200

    def test_UpdateRoleFail(self):
        user1 = mixer.blend(Role, filters={'nam': 'l'})
        user_id = user1.id

        url = reverse('update-role', kwargs={'pk': user_id})
        print("url", url)
        data = {'name': 'k', 'module': 'Movie', }
        response = self.client.put(url, data=data)
        print("response", dir(response))
        assert response.status_code == 400

    def test_deleteARole(self):
        user1 = mixer.blend(Role, filters={'nam': 'l'})
        url = reverse('delete-role', kwargs={'pk': user1.id})
        print("url", url)
        response = self.client.delete(url)
        print("response", dir(response))
        assert response.status_code == 204

    def test_add_role_to_user(self):
        # user1 = mixer.blend(CustomUser, first_name='Prasad', email='a@a.com')
        user_eg = CustomUser.objects.create_user(first_name='pr', last_name='la', email='a@p.com', level='AD',
                                                 password=123)
        role_eg = Role.objects.create(id=1, name='can_view_data', module='Movie', kind='View', priority=4,
                                      filters={"name__startswith": "m"})
        print(role_eg.id)
        #
        url = reverse('add_role_to_user')
        print("url", url)

        data = {'role': 1, 'user': 'a@p.com'}

        response = self.client.post(url, data=data)
        a = CustomUser.objects.get(email=data['user'])
        a.role.add(data['role'])
        print("response", dir(response))
        print(response.status_code)

        assert 201 == 201

    def test_remove_role_from_user(self):
        user_eg = CustomUser.objects.create_user(first_name='pr', last_name='la', email='a@p.com', level='AD',
                                                 password=123)
        role_eg = Role.objects.create(id=1, name='can_view_data', module='Movie', kind='View', priority=4,
                                      filters={"name__startswith": "m"})
        print(role_eg.id)

        url = reverse('remove_role_from_user')
        print("url", url)

        data = {'role': 1, 'user': 'a@p.com'}
        response = self.client.post(url, data=data)
        a = CustomUser.objects.get(email=data['user'])
        a.role.remove(data['role'])
        print("response", dir(response))
        print(response.status_code)

        assert 201 == 201

    def test_listing_privileges_bestowed_on_a_role(self):
        user_eg = CustomUser.objects.create_user(first_name='pr', last_name='la', email='a@p.com', level='AD',
                                                 password=123)
        role_eg = Role.objects.create(id=1, name='can_view_data', module='Movie', kind='View', priority=4,
                                      filters={"name__startswith": "m"})

        url = reverse('listing_privileges_bestowed_on_a_role')
        print("url", url)

        response = self.client.get(url)
        print("response", dir(response))
        print(response.status_code)

        assert 200 == 200

    def test_listing_all_users_associated_with_a_role(self):
        user_eg = CustomUser.objects.create_user(first_name='pr', last_name='la', email='a@p.com', level='AD',
                                                 password=123)
        role_eg = Role.objects.create(id=1, name='can_view_data', module='Movie', kind='View', priority=4,
                                      filters={"name__startswith": "m"})
        url = reverse('listing_all_users_associated_with_a_role')
        print("url", url)

        response = self.client.get(url)
        print("response", dir(response))
        print(response.status_code)

        assert 200 == 200
