# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals)
from . import api_keys
# Cache backend (Azure Functions) API

rest_url = {
    'cache_get_program': api_keys.CACHE_API_BASE_URL + '/Program/{0}',
    'cache_get_program_list': api_keys.CACHE_API_BASE_URL + '/Program/List/{0}'
}
