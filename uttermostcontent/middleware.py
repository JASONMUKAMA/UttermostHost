import logging

from django.http import HttpResponseServerError

import socket
import errno

try:
    # Your code that might cause a broken pipe error
    pass
except IOError as e:
    if e.errno != errno.EPIPE:
        raise

class HandleBrokenPipeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except IOError as e:
            if 'broken pipe' in str(e).lower():
                logging.warning('Broken pipe error occurred')
                return HttpResponseServerError("Server error")
            raise
