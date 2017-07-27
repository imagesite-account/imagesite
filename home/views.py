import json

from django.shortcuts import render

from master import GLOBAL_CURRENT_HOST, IMAGE_ERR_CODES
from album import EMPTY_ALBUM_KEY
from .api import api_get_album


def index(request):
    albums = []
    vars_dict = {'albums': albums, 'global_current_host': GLOBAL_CURRENT_HOST}
    if request.method == "POST":
        return render(request, 'home.html', vars_dict)
    else:
        return render(request, 'home.html', vars_dict)
