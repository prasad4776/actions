from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=20)
    rank = models.IntegerField(default=1)

    def __str__(self):
        return self.name
