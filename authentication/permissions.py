from rest_framework.permissions import BasePermission
from .models import CustomUser


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.level == CustomUser.ADMIN
