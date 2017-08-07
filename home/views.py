import json

from django.shortcuts import render

from .api import api_get_all_album

from master import GLOBAL_CURRENT_HOST, IMAGE_ERR_CODES, contact
from album import EMPTY_ALBUM_KEY


def index(request):
    # albums = get_all_album_basic(nxm_format=4)
    vars_dict = {
        'album_id': 'None (this is the homepage)',
        # 'albums': albums,
        # 'albums': api_get_all_album(None),
        'global_current_host': GLOBAL_CURRENT_HOST,
        'contact': contact,
    }
    if request.method == "POST":
        return render(request, 'home.html', vars_dict)
    else:
        return render(request, 'home.html', vars_dict)
