from django.test import TestCase
import pytest
from mixer.backend.django import mixer
from movies.models import Movie

# Create your tests here.

pytestmark = pytest.mark.django_db


class TestMovie(TestCase):

    def test_str(self):
        user1 = mixer.blend(Movie, name="Test", rank=1)
        user_result = Movie.objects.last()

        assert user_result.__str__() == 'Test'
