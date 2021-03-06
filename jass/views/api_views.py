from rest_framework.views import APIView
from rest_framework import viewsets
from jass.serializers import *
from rest_framework.response import Response
from jass.models import *
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404


class CurrentUserView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PlayerSeriesViewSet(viewsets.ViewSet):
    """
    API endpoint for player games
    """

    def list(self, request):
        queryset = Series.get_series_for_player(request.user)
        serializer = SeriesSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class AvailableSeriesViewSet(viewsets.ViewSet):
    """
    API endpoint for available/open series
    """

    def list(self, request):
        queryset = Series.get_available_series()
        serializer = SeriesSerializer(queryset, many=True)
        return Response(serializer.data)