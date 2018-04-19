from rest_framework.documentation import include_docs_urls

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='docs')),
    url(r'^api/', include('rest_framework.urls')),
    url(r'^api/imdb/', include('imdb.urls')),
    url(r'^api/tmdb/', include('tmdb.urls')),
    url(r'^api/remakes/', include('remake.urls')),
    url(r'^docs/', include_docs_urls(title='Fantasy Cast'))
]
