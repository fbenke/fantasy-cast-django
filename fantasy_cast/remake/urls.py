from django.conf.urls import url
from remake import views

urlpatterns = [
    url(r'^$', views.RemakeList.as_view()),
    url(r'^(?P<pk>[0-9]+)$', views.RemakeDetail.as_view()),
    url(r'^(?P<pk>[0-9]+)/actor_suggestions/$',
        views.GetActorSuggestions.as_view()),
]
