import json
from time import gmtime, strftime

from urllib.request import unquote

from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.renderers import JSONRenderer

from .models import ViewData, create_or_get_model
from .serializers import ViewDataSerializer, InterimMessagesSerializer

from master import check_sql, format_id


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

##############################################
# API/JSON Methods


def api_get_album(request, album_id):

    album = None
    try:
        album = ViewData.objects.get(pk=album_id)
    except Exception as ex:
        pass

    serializer = ViewDataSerializer(album)

    return JSONResponse(serializer.data)


def api_get_all_album(request):
    album_list = []
    try:
        album_list = ViewData.objects.all()
    except Exception as ex:
        pass

    serializer = ViewDataSerializer(album_list, many=True)

    return JSONResponse(serializer.data)

##############################################
# non-API/JSON Methods


# def get_all_album_basic_formatted(request, nxm_format):
#     # album_list = []
#     # try:
#     #     album_list = [album.get_basic_info() for album in ViewData.objects.all()]
#     #     print('[view/api.py/get_all_album]: Album_list', album_list)
#     # except Exception as ex:
#     #     print('[view/api.py/get_all_album] Error retrieving album list:',)
#     #     print(ex)
#     #     return None
#     #
#     # if nxm_format is None:
#     #     pass
#     # elif isinstance(nxm_format, int):
#     #     album_list_ = []
#     #
#     #     for i, album in enumerate(album_list):
#     #         k = i // nxm_format
#     #         if i % nxm_format == 0:
#     #             album_list_.append([])
#     #         album_list_[k].append(album)
#     #         print('[view/api.py/get_all_album]: Album', album)
#     #
#     #         album_list = album_list_
#     #
#     # print('[view/api.py/get_all_album]: Album_list', album_list)
#     # # print(album_list)
#
#     return album_list
################################


@csrf_exempt
def api_submit_rating(request, album_id): # album_id, rating in request
    success = False
    # current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    # image_id = request.POST.get('image_id', 'Empty')
    # rating = request.POST.get('rating', '-1')
    #
    if not request.POST.dict().items():
        message_dict = {'success': success, 'image': '',
                        'additional_message': 'You haven\'t passed any rating for the API to process!'}
        im_data = InterimMessagesContent(message_dict)
        serializer = InterimMessagesSerializer(im_data)
        return JSONResponse(serializer.data)

    req_str = ''
    for key, val in request.POST.dict().items():
        req_str = key
        break

    print('[view/api.py/api_submit_rating] request.POST.dict():', request.POST.dict())
    print('[view/api.py/api_submit_rating] req_str:', str(req_str).strip())
    req_dict = json.loads(str(req_str).strip())
    print('[view/api.py/api_submit_rating] req_dict:', req_dict)

    image_id = req_dict['image_id']
    rating = req_dict['rating']

    image_id = format_id(image_id)

    print(image_id, rating)

    # if album_id != album_id_:
    #     # Return "failed"
    #     pass

    #
    # try:
    #     album_id = check_sql(album_id)
    #     with conns['album_image_data'].cursor() as c:
    #         c.execute('''CREATE TABLE IF NOT EXISTS {table_name}
    #                     (rating INT, datetime TEXT, extra TEXT)
    #                     '''
    #                   .format(table_name=album_id))
    #     success = True
    #     print('[View/api.py/api_submit_rating] Added db table', album_id)
    # except Exception as ex:
    #     print('[View/api.py/api_submit_rating] Error:', ex)
    #     success = True

    Album_Model = create_or_get_model(album_id)
    if Album_Model is None:
        print('[view/api.py/api_submit_rating] Error occured trying to create or get model for album_id:', album_id)
        success = False
    else:
        album = Album_Model(rating=rating, datetime=str(timezone.now()), image_id=image_id)
        album.save()
        print('[view/api.py/api_submit_rating] Successfully added rating for {album_id}!'.format(album_id=album_id))
        print('[view/api.py/api_submit_rating] Rating:', rating, album.rating)
        success = True

    # TODO: Return True/false as a response if successful/unsuccessful in storing rating
    message_dict = {'success': success, 'image': image_id, 'additional_message:': ''}
    im_data = InterimMessagesContent(message_dict)
    serializer = InterimMessagesSerializer(im_data)
    print(serializer.data)

    return JSONResponse(serializer.data)

