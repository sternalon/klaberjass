from django.urls import path
from jass.views.views import *

urlpatterns = [
    # path('', index, name='index'),
    # url(r'^register/', CreateUserView.as_view()),
    path('register/', CreateUserView.as_view()),
    path('login/', LoginUserView.as_view(), name="login"),
    path('logout/', LogoutUserView.as_view(next_page='/jass'), name="logout"),
    path('', HomeView.as_view())
]