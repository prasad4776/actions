from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import RoleSerializer, RoleFilterSerializer, RoleSerializerForListingUsers
from rest_framework.response import Response
from authentication.models import CustomUser as User
from .models import Role


# Create your views here.
class RoleView(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            raise Http404

    def get(
            self, request,
    ):
        role = Role.objects.all()
        serializer = RoleSerializer(role, many=True)
        return Response({"role": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        role = self.get_object(pk)
        print(request.data)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"updated_data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        print(pk)
        role = self.get_object(pk)
        role.delete()
        return Response({"role deleted with id": pk}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@csrf_exempt
def add_role_to_user(request):
    """

    :return: Adds the given role to the user.
    """
    print(request.POST)
    print(dir(request))
    r_name = request.POST["role"]
    u_name = request.POST["user"]
    user_to_process = User.objects.get(email=u_name)
    print(user_to_process)
    user_to_process.role.add(r_name)

    return Response({"added user to role": u_name}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@csrf_exempt
def remove_role_from_user(request):
    """

    :return: Removes the given role from the user.
    """
    print(request.POST)
    print(dir(request))
    r_name = request.POST["role"]
    u_name = request.POST["user"]
    user_to_process = User.objects.get(email=u_name)
    user_to_process.role.remove(r_name)

    return Response({"removed role from user": u_name}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def listing_privileges_bestowed_on_a_role(request):
    """

    :return: Lists all privileges bestowed on a role.
    """
    roles = Role.objects.only('name', 'filters')
    serializer = RoleFilterSerializer(roles, many=True)
    return Response({"roles with permissions": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def listing_all_users_associated_with_a_role(request):
    """
    :return: Lists all users associated with a role.
    """
    # employees = User.objects.all().values('id', 'role__name')
    # # print(employees)
    emp = Role.objects.all()
    serializer = RoleSerializerForListingUsers(emp, many=True)
    return Response({"role with user data": serializer.data}, status=status.HTTP_200_OK)
