import argparse
import socket
import time
import multiprocessing
import importlib


class Worker:

    def __init__(self, server_socket, web_app):
        self.server_socket = server_socket
        self.web_app = web_app

    def __call__(self):
        while True:
            client_socket, addr = self.server_socket.accept()  # <---- blocking
            try:
                data = client_socket.recv(1024)
                data_decoded = data.decode('utf8')
                print(f'Got data from {addr}')
                print(data_decoded)

                lines = data_decoded.split('\r\n')
                method, path, http_version = lines[0].split(' ')

                # here is the strange place
                # there is WSGI
                status, body = self.web_app.handle(method, path)

                response = (
                    f'{http_version} {status}\r\n'
                    'Content-Type: text/html; charset:utf-8\r\n'
                    '\r\n'
                    f'{body}'
                )

                client_socket.sendall(response.encode('utf8'))
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
                multiprocessing.Process(target=Worker(server_socket, web_app), daemon=True)
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
