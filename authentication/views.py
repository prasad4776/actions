from .models import CustomUser as User
from .serializers import CustomUserSerializer
from .permissions import IsAdmin
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
import json


class AllUsers(ListAPIView, CreateAPIView):
    """
    Lists all user
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class AdminUser(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin,)

    def get(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        :return: Deletes a user
        """

        instance = self.get_object()
        instance.delete()
        return Response({"detail": "User Deleted"})

    def update(self, request, *args, **kwargs):
        """
        :return: Updates a user
        """

        print(request.data)
        instance = self.get_object()
        if request.data.get("new_password"):
            instance.set_password(request.data.get("new_password"))
        if request.data.get("new_groups"):
            instance.groups = request.data
        if request.data.get("new_level"):
            instance.level = request.data.get("new_level")
        instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
