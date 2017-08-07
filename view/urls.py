from django.conf.urls import url

from . import views, api


# test album: http://imgur.com/a/VBrKp
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^api/0/(?P<album_id>[\w|\W]+)/$', api.api_get_album),
    url(r'^api/1/(?P<album_id>[\w|\W]+)/$', api.api_submit_rating),
    url(r'^api/2/', api.api_get_all_album),
    # url(r'^api/3/(?P<nxm_format>\d+)', api.get_all_album_basic_formatted),
    url(r'^(?P<album_id>[\w|\W]+)/', views.index, name='index'),
    # url(r'^album/(?P<album_id>[\w|\W]+)/$', views.view_album),

]