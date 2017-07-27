from django.conf.urls import url

from . import views, api


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
