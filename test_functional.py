
# import pytest
import socket
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

#     socket_conn.listen(1)

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


def test_function():
    ADDR = ('127.0.0.1', 8000)
    client_conn = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

    client_conn.connect(ADDR)

    msg = "do you hear me?"

    try:
        client_conn.sendall(msg)
        output = ""
        while True:
            part = client_conn.recv(16)
            output = output + part
            if len(part) < 16:
                sys.stdout.write(output)
                client_conn.shutdown(socket.SHUT_WR)
                client_conn.close()
                break
    except Exception as e:
        print e
    assert output[-15:] == msg
