from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import pre_save


# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=20)
    module = models.CharField(max_length=20)
    kind = models.CharField(max_length=20)
    priority = models.PositiveIntegerField()
    filters = JSONField(null=True)

    def __str__(self):
        return self.name


def update_prirority(sender, instance, **kwargs):
    """

    :param sender: Name of the sender model(CLass)
    :param instance: instance of that object
    :param kwargs:
    :return: calculates the length of the filters and
             then updates the value of priority,
             equal to the length of the filters.
    """
    x = len(instance.filters)
    instance.priority = x


pre_save.connect(update_prirority, sender=Role)
