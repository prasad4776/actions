from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MovieSerializer
from .models import Movie
from authentication.models import get_permission
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class FilmView(APIView):
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(
            self, request,
    ):
        """
        :return: Displays a list of all movies or by the users role.
        """
        perm = get_permission(request.user, "Movie", "View")
        if perm is not None:
            queryset = Movie.objects.all()
            queryset = queryset.filter(Q(**perm.filters))
            serializer = MovieSerializer(queryset, many=True)
            return Response({"movies": serializer.data}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied

    def post(self, request):
        """
        :return: Creates instance of movie with given details.
        """
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, ):
        """

        :param pk: id of the movie
        :return: Updates movie for the given id(pk)

        """
        film = self.get_object(pk)
        serializer = MovieSerializer(film, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"updated_data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        :param pk: id of the movie
        :return: Deletes a movie by the given id(pk).
        """
        film = self.get_object(pk)
        film.delete()
        return Response({'movie deleted with id': pk}, status=status.HTTP_204_NO_CONTENT)


def home(request):
    return HttpResponse('Hello its me.........')
