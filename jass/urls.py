from django.urls import path
from jass.views.api_views import *
from jass.views.views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('register/', CreateUserView.as_view()),
    path('login/', LoginUserView.as_view(), name="login"),
    path('logout/', LogoutUserView.as_view(next_page='/'), name="logout"),
    path('lobby/', LobbyView.as_view()),
    path('hello/', HelloView.as_view()),
    path('series/<int:series_id>/', SeriesView.as_view()),
    path('', HomeView.as_view())
]

# urls for api - django rest framework
urlpatterns += [
    path('current-user/', CurrentUserView.as_view()),
    path('series-from-id/<int:series_id>/', SingleSeriesViewSet.as_view()),
    path('game-from-id/<int:game_id>/', SingleGameViewSet.as_view()),
]

router = DefaultRouter()
router.register(r'player-series', PlayerSeriesViewSet, 'player_series')
router.register(r'available-series', AvailableSeriesViewSet, 'available_series')

urlpatterns += router.urls