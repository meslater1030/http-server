
# import pytest
import socket
<<<<<<< HEAD
#import server
from multiprocessing import Process
#from server import response_ok


def run_server():
    ADDR = ('127.0.0.1', 8000)
    socket_conn = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

    socket_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    socket_conn.bind(ADDR)
=======
import sys
# import server
# # from server import response_ok
# from multiprocessing import Process


# @pytest.yield_fixture
# def server_process():
#     process = Process(target=server.start_server)
#     process.daemon = True
#     process.start()
#     yield process

# @pytest.fixture(scope="module")
# def test_run_server(request):
#     ADDR = ('127.0.0.1', 8000)
#     socket_conn = socket.socket(
#         socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
#     )

#     socket_conn.bind(ADDR)
>>>>>>> a79b0f0b7d747246cd2955f62857b1dfd154d938

#     socket_conn.listen(1)

<<<<<<< HEAD
    while True:
        try:
            conn, addr = socket_conn.accept()
            output = ""
            while True:
                msg = conn.recv(16)
                output = output + msg
                if len(msg) < 16:
                    #response_ok()
                    conn.sendall(output)
                    conn.close()
                    break
        except KeyboardInterrupt:
            break
=======
#     while True:
#         try:
#             conn, addr = socket_conn.accept()
#             output = ""
#             while True:
#                 msg = conn.recv(16)
#                 output = output + msg
#                 if len(msg) < 16:
#                     response_ok()
#                     conn.sendall(output)
#                     conn.close()
#                     break
#         except KeyboardInterrupt:
#             break
>>>>>>> a79b0f0b7d747246cd2955f62857b1dfd154d938


@pytest.yield_fixture()
def multiproc():
    special_process = Process(target=run_server)
    special_process.daemon = True
    special_process.start()
    yield special_process


def test_response_ok(multiproc):
    pass


def test_response_error():
    pass


@pytest.fixture()
def client_code():
    ADDR = ('127.0.0.1', 8000)
    client_conn = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

    client_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_conn.connect(ADDR)
    return client_conn


<<<<<<< HEAD
def test_function(client_code):
    msg = "do you hear me at all?"
=======
    msg = "do you hear me?"
>>>>>>> a79b0f0b7d747246cd2955f62857b1dfd154d938

    try:
        client_code.sendall(msg)
        output = ""
        while True:
<<<<<<< HEAD
            part = client_code.recv(16)
            assert part
            output = output + part
            if len(part) < 16:
                client_code.shutdown(socket.SHUT_WR)
                client_code.close()
                break
        assert '<html>' in output
=======
            part = client_conn.recv(16)
            output = output + part
            if len(part) < 16:
                sys.stdout.write(output)
                client_conn.shutdown(socket.SHUT_WR)
                client_conn.close()
                break
>>>>>>> a79b0f0b7d747246cd2955f62857b1dfd154d938
    except Exception as e:
        print e
    assert output[-15:] == msg
