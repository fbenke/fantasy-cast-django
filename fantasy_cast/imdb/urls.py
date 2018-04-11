from django.conf.urls import url
from imdb import views

urlpatterns = [
    url(r'^movies/$', views.MovieSuggestions.as_view())
]
