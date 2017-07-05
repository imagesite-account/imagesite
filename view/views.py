import json

from django.http import HttpResponse, QueryDict
from django.shortcuts import render

from album import EMPTY_ALBUM_KEY
from .api import api_get_album

def index(request):

    if request.method == "POST":
        return render(request, 'view.html')
    else:
        return render(request, 'view.html')


# def view_album(request, album_id=EMPTY_ALBUM_KEY):
#     if request.method == "POST":
#         return render(request, 'view.html', {'album_id': album_id})
#     else:
#         return render(request, 'view.html', {'album_id': album_id})


def process_request(request):
    if 'application/json' in request.META['CONTENT_TYPE']:
        # load the json data
        # http://stackoverflow.com/questions/24069197/httpresponse-object-json-object-must-be-str-not-bytes
        data = json.loads(request.body.decode())
        # for consistency sake, we want to return
        # a Django QueryDict and not a plain Dict.
        # The primary difference is that the QueryDict stores
        # every value in a list and is, by default, immutable.
        # The primary issue is making sure that list values are
        # properly inserted into the QueryDict.  If we simply
        # do a q_data.update(data), any list values will be wrapped
        # in another list. By iterating through the list and updating
        # for each value, we get the expected result of a single list.
        q_data = QueryDict('', mutable=True)
        # http://stackoverflow.com/questions/30418481/error-dict-object-has-no-attribute-iteritems-when-trying-to-use-networkx
        for key, value in data.items():
            if isinstance(value, list):
                # need to iterate through the list and upate
                # so that the list does not get wrapped in an
                # additional list.
                for x in value:
                    q_data.update({key: x})
            else:
                q_data.update({key: value})

        if request.method == 'GET':
            request.GET = q_data

        if request.method == 'POST':
            request.POST = q_data

    return None