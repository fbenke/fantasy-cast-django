from django.conf.urls import url
from tmdb import views

urlpatterns = [
    url(r'^movies/$', views.MovieSuggestions.as_view())
]
