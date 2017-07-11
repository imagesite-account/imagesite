import json

from django.shortcuts import render

from master import GLOBAL_CURRENT_HOST, IMAGE_ERR_CODES
from album import EMPTY_ALBUM_KEY
from .api import api_get_album


def index(request, album_id = 'VBrKp'):
    vars_dict = {'album_id': album_id, 'global_current_host': GLOBAL_CURRENT_HOST}
    if request.method == "POST":
        return render(request, 'view.html', vars_dict)
    else:
        return render(request, 'view.html', vars_dict)


# def view_album(request, album_id=EMPTY_ALBUM_KEY):
#     if request.method == "POST":
#         return render(request, 'view.html', {'album_id': album_id})
#     else:
#         return render(request, 'view.html', {'album_id': album_id})

