from django.conf.urls import url

from . import views, api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^album/(?P<album_id>[\w|\W]+)/$', views.view_album),
    url(r'^album/api/(?P<album_id>[\w|\W]+)/$', api.api_get_album),
]