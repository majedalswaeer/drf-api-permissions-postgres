from django.urls import path
from .views import GamesList, GamesDetail

urlpatterns = [
    path('', GamesList.as_view(), name='games_list'),
    path('<int:pk>/', GamesDetail.as_view(), name='games_detail'),
]