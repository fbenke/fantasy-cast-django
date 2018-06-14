from django.conf.urls import url
from tmdb import views

urlpatterns = [
    url(r'^movies/$', views.MovieSuggestions.as_view()),
    url(r'^movie/(?P<imdb_id>[0-9]+)/$', views.GetMovie.as_view())
]
