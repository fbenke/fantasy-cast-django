from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^api/', include('rest_framework.urls')),
    url(r'^api/imdb/', include('imdb.urls')),
    url(r'^api/tmdb/', include('tmdb.urls'))
]
