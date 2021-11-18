import os
import time
from typing import Dict, Callable, Iterable


class WebApp:

    def __init__(self):
        pass

    def __call__(self, environ: Dict, start_response: Callable) -> Iterable:
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        status, body = self.handle(method, path)
        response_headers = [
            ('Content-Type', 'text/html; charset=utf-8'),
        ]
        start_response(status, response_headers)

        return [body.encode('utf8')]

    def handle(self, method: str, path: str, http_headers: dict=None):
        pid = os.getpid()
        if path == '/':
            status = '200 OK'
            body = f'<html><body><h1>Hello World from {pid}</h1></body></html>'
        elif path == '/slow':
            status = '200 OK'
            body = f'<html><body><h1>Im slow from {pid}...</h1></body></html>'
            print('Sleeping 5 secs...')
            time.sleep(5)
        else:
            status = '404 Not Found'
            body = f'<html><body><h1>Oops, page is lost from {pid}</h1></body></html>'
        return status, body


web_app = WebApp()
