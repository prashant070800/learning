# api_logger/monkey_patch_requests.py

import requests
import threading
from django.db import connection
from .models import ExternalAPIRequestLog

_original_get = requests.get

def _log_response(url, headers, params, response):
    def _log():
        connection.close()
        ExternalAPIRequestLog.objects.create(
            url=url,
            request_headers=headers or {},
            request_params=params or {},
            response_status=response.status_code,
            response_body=response.text,
        )
    threading.Thread(target=_log).start()

def custom_get(url, **kwargs):
    headers = kwargs.get('headers')
    params = kwargs.get('params')
    response = _original_get(url, **kwargs)
    _log_response(url, headers, params, response)
    return response

requests.get = custom_get
