import argparse
import socket
import time


def request(host, port):
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    ) as client_socket:
        client_socket.connect((host, port))

        http_req_part_1 = (
            b'GET / HTTP/1.1\r\n'
            b'Host: 127.0.0.1\r\n'
            b'Content-Type: text/plain\r\n'
        )
        print('Sending')
        print(http_req_part_1)
        client_socket.send(http_req_part_1)

        print('Sleeping 20 sec...')
        time.sleep(20)

        http_req_part_2 = (
            b'\r\n'
        )
        print('Sending')
        print(http_req_part_2)
        client_socket.send(http_req_part_2)

        data = client_socket.recv(1024)
        print('Got data:')
        print(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bind', help='Host and port to listen to, for example "0.0.0.0:8080"')
    args = parser.parse_args()
    host, port = args.bind.split(':')
    request(host, int(port))
