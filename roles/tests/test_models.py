from django.test import TestCase
import pytest
from mixer.backend.django import mixer
from roles.models import Role

# Create your tests here.

pytestmark = pytest.mark.django_db


class TestRole(TestCase):

    def test_str(self):
        user1 = mixer.blend(Role, name="Test",
                            filters={'nam': 'l'})
        user_result = Role.objects.last()

        assert user_result.__str__() == 'Test'
