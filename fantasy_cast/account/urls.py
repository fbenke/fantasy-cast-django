from django.conf.urls import url
from account import views

urlpatterns = [
    url(r'^signup/$', views.Signup.as_view()),
    url(r'^signin/$', views.Signin.as_view()),
    url(r'^signout/$', views.Signout.as_view())
]
