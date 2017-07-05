import json
from urllib.request import unquote

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from .models import ViewData
from .serializers import ViewDataSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        # print('Stats API JSONResponse:', data)
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def api_get_album(request, album_id):

    album = None
    try:
        album = ViewData.objects.get(pk=album_id)
    except Exception as ex:
        pass

    serializer = ViewDataSerializer(album)

    return JSONResponse(serializer.data)
