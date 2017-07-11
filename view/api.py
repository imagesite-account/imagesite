import json
from time import gmtime, strftime

from urllib.request import unquote

from django.http import HttpResponse, QueryDict
from django.db import connections as conns
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

from .models import ViewData
from .serializers import ViewDataSerializer, InterimMessagesSerializer


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


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        # print('Stats API JSONResponse:', data)
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class InterimMessagesContent(object):
    def __init__(self, messages):
        self.messages = messages


def api_get_album(request, album_id):

    album = None
    try:
        album = ViewData.objects.get(pk=album_id)
    except Exception as ex:
        pass

    serializer = ViewDataSerializer(album)

    return JSONResponse(serializer.data)


################################

@csrf_exempt
def api_submit_rating(request, album_id): # album_id, rating in request
    success = False
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    # image_id = request.POST.get('image_id', 'Empty')
    # rating = request.POST.get('rating', '-1')
    #
    req_str = ''
    for key, val in request.POST.dict().items():
        req_str = key
        break

    req_dict = json.loads(req_str)

    image_id = req_dict['image_id']
    rating = req_dict['rating']

    print('[api_submit_rating]:', request.POST.dict())
    print(image_id, rating)

    # if album_id != album_id_:
    #     # Return "failed"
    #     pass


    try:
        with conns['album_image_data'].cursor() as c:
            c.execute('''CREATE TABLE IF NOT EXISTS %s
                        (rating INT, datetime TEXT)
                        ''',
                      [album_id, ])
        success = True
    except Exception as ex:
        print('[api_submit_rating] Error:', ex)
        success = True
    # TODO: Return True/false as a response if successful/unsuccessful in storing rating
    message_dict = {'success': success, 'image': image_id, 'additional_message:': ''}
    im_data = InterimMessagesContent(message_dict)
    serializer = InterimMessagesSerializer(im_data)
    print(serializer.data)

    return JSONResponse(serializer.data)

