from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from uuid import uuid4
import django.contrib.postgres.fields as postgres
from django.db.models.signals import pre_save
from roles.models import Role


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    @staticmethod
    def get_user(id_):
        try:
            return CustomUser.objects.get(pk=id_)  # <-- tried to get by email here
        except CustomUser.DoesNotExist:
            return None


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = None
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    ADMIN = "AD"
    MANAGER = "MG"
    LEVEL_CHOICES = (
        (L1, "L1"),
        (L2, "L2"),
        (L3, "L3"),
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
    )
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=L1)
    role = models.ManyToManyField(Role, related_name="users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["level", "first_name", "last_name"]
    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name() + " (" + self.get_level_display() + ")"

    def display_name(self):
        return self.get_full_name() + " (" + self.get_level_display() + ")"

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def is_admin(self):
        return self.level == "AD"

    class Meta:
        ordering = ["email"]


def get_permission(user, module, kind):
    return user.role.filter(module=module, kind=kind).order_by("-priority").first()
