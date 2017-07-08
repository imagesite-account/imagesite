from django.conf.urls import url

from . import views, api


# test album: http://imgur.com/a/VBrKp
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/0/(?P<album_id>[\w|\W]+)/$', api.api_get_album),
    url(r'^(?P<album_id>[\w|\W]+)/$', views.index, name='index'),
    # url(r'^album/(?P<album_id>[\w|\W]+)/$', views.view_album),

]