from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly
# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Game
from .serializers import GameSerializer

class GamesList(ListCreateAPIView):
    permission_classes =(IsAuthorOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GamesDetail(RetrieveUpdateDestroyAPIView):
    permission_classes =(IsAuthorOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer