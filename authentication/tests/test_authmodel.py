from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from authentication.models import CustomUser
import pytest
from mixer.backend.django import mixer

# Create your tests here.

pytestmark = pytest.mark.django_db


class TestCustomUserModel(TestCase):
    # def setUp(self):
    #     self.user1 = CustomUser.objects.create_user(email="test@parham.in", first_name="Test", last_name="User",
    #                                                 password="Test.User", level='L1')

    def test_create_user(self):
        user1 = mixer.blend(CustomUser, first_name='Test')

        user_result = CustomUser.objects.last()

        assert user_result.first_name == 'Test'

    def test_display_name(self):
        user1 = mixer.blend(CustomUser, first_name="Test", last_name="User", level='L1')

        user_result = CustomUser.objects.last()

        assert user_result.display_name() == 'Test User (L1)'

    def test_get_full_name(self):
        user1 = mixer.blend(CustomUser, first_name="Test", last_name="User", )
        user_result = CustomUser.objects.last()

        assert user_result.get_full_name() == 'Test User'

    def test_is_admin(self):
        user1 = mixer.blend(CustomUser, level='L1')
        user_result = CustomUser.objects.last()

        assert user_result.is_admin() != 'L1'

    def test_str(self):
        user1 = mixer.blend(CustomUser, first_name="Test", last_name="User", level='L1')
        user_result = CustomUser.objects.last()

        assert user_result.__str__() == 'Test User (L1)'
