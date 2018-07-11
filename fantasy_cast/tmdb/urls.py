from django.conf.urls import url
from tmdb import views

urlpatterns = [
    url(r'^movies/$', views.MovieSuggestions.as_view()),
    url(r'^movie/imdb/(?P<imdb_id>[0-9]+)/$',
        views.GetMovieForImdbId.as_view()),
    url(r'^movie/remake/(?P<pk>[0-9]+)/$',
        views.GetMovieForRemake.as_view())
]
