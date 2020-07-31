from rest_framework import serializers
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RoleFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'filters')


class RoleSerializerForListingUsers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'users')
        depth = 1
