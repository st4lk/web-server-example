import argparse
import socket
import time
import multiprocessing
import importlib
import io
from typing import Dict, Tuple, List, Optional


class Response:

    def __init__(self, data, web_app, host, port):
        self.data = data
        self.web_app = web_app
        self.host = host
        self.port = port
        self.status: Optional[str] = None
        self.response_headers: Optional[List[Tuple]] = None

    def __iter__(self):

        environ = self.get_environ()
        web_app_response = self.web_app(environ, self.start_response)
        http_version = environ['SERVER_PROTOCOL']
        for index, resp_part in enumerate(web_app_response):
            if index == 0:
                headers = f'{http_version} {self.status}\r\n'
                for header_name, header_value in self.response_headers:
                    headers += f'{header_name}: {header_value}\r\n'
                headers += '\r\n'
                yield headers.encode('ascii')
            yield resp_part

    def start_response(self, status, response_headers):
        assert self.status is None
        assert self.response_headers is None
        self.status = status
        self.response_headers = response_headers

    def get_environ(self) -> Dict:
        raw_headers, raw_body = self.data.split(b'\r\n\r\n', 1)
        decoded_headers = raw_headers.decode('ascii').split('\r\n')
        method, path, http_version = decoded_headers[0].split(' ')
        headers = {}
        for header_row in decoded_headers[1:]:
            name, value = header_row.split(':', 1)
            headers[name] = value.strip()

        environ = {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'QUERY_STRING': '',
            'CONTENT_TYPE': headers.get('Content-Type', ''),
            'CONTENT_LENGTH': headers.get('Content-Length', ''),
            'SERVER_NAME': self.host,
            'SERVER_PORT': self.port,
            'SERVER_PROTOCOL': http_version,
        }
        environ.update({
            f'HTTP_{name}'.upper(): value for name, value in headers.items()
        })
        environ.update({
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': io.BytesIO(raw_body),
            'wsgi.errors': io.StringIO(''),
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        })
        return environ


class Worker:

    def __init__(self, server_socket, web_app, host, port):
        self.server_socket = server_socket
        self.web_app = web_app
        self.host = host
        self.port = port

    def __call__(self):
        while True:
            client_socket, addr = self.server_socket.accept()  # <---- blocking
            try:
                data = client_socket.recv(1024)
                data_decoded = data.decode('utf8')
                print(f'Got data from {addr}')
                print(data_decoded)

                resp = Response(data, self.web_app, self.host, self.port)
                for resp_part in resp:
                    client_socket.sendall(resp_part)
            finally:
                client_socket.close()


class WebServer:

    def __init__(self, host, port, web_app, num_workers):
        self.host = host
        self.port = int(port)
        self.web_app = web_app
        self.num_workers = num_workers
        self.workers = []

    def run(self):
        with socket.socket(
            socket.AF_INET,  # IP
            socket.SOCK_STREAM,  # TCP
        ) as server_socket:
            print(f'Listening on http://{self.host}:{self.port}')
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(4)

            self.workers = [
                multiprocessing.Process(target=Worker(server_socket, web_app, self.host, self.port), daemon=True)
                for i in range(self.num_workers)
            ]

            for worker in self.workers:
                worker.start()

            while True:
                time.sleep(15)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('web_app_path')
    args = parser.parse_args()

    web_app_module_name, web_app_func_name = args.web_app_path.split(':')

    web_app_module = importlib.import_module(web_app_module_name)
    web_app = getattr(web_app_module, web_app_func_name)

    server = WebServer('0.0.0.0', 9999, web_app=web_app, num_workers=4)
    server.run()
