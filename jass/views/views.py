from django.http import HttpResponse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user
from django.contrib import messages

from jass.models import User, Series
from jass import signals


class HomeView(TemplateView):
    template_name = 'home.html'


class HelloView(TemplateView):
    template_name = 'card.html'



class CreateUserView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        valid = super(CreateUserView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

class LoginUserView(LoginView):
    template_name = 'login.html'

class LogoutUserView(LogoutView):
    template_name = 'home.html'


class LobbyView(TemplateView):
    template_name = 'lobby.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LobbyView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LobbyView, self).get_context_data(**kwargs)
        # get current open games to prepopulate the list

        # we're creating a list of games that contains just the id (for the link) and the creator
        # available_games = [{'creator': game.creator.username, 'id': game.pk} for game in Game.get_available_games()]
        # for the player's games, we're returning a list of games with the opponent and id
        # player_games = Game.get_games_for_player(self.request.user)

        return context


class SeriesView(TemplateView):
    template_name = 'series.html'
    series = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # get the game by the id
        self.series = Series.get_by_id(kwargs['series_id'])
        user = get_user(request)
        # check to see if the series is open and available for this user
        # if this player is the creator, just return
        if self.series.player_in_series(user):
            return super(SeriesView, self).dispatch(request, *args, **kwargs)

        # if there is no opponent and the series is not yet completed,
        # set the opponent as this user

        #Check if series is not yet full, and adds player to series
        if not self.series.is_full() and not self.series.completed:
            self.series.add_next_user(user)
            signals.send_available_series_update()
            return super(SeriesView, self).dispatch(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'Sorry, the selected series is not available.')
            return redirect('/lobby/')

    def get_context_data(self, **kwargs):
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['series'] = self.series

        return context



def index(request):
    return HttpResponse("Hello, Jules, you are a legend.")


