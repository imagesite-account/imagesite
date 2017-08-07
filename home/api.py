import json
from time import gmtime, strftime

from urllib.request import unquote

from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.renderers import JSONRenderer

from .models import ViewData

from view.api import *
from view.serializers import MultipleViewDataSerializer

from master import check_sql, format_id


