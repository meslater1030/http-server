#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import socket
<<<<<<< Updated upstream
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

    socket_conn.listen(1)

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
=======
import sys
# import server
# # from server import response_ok
# from multiprocessing import Process


@pytest.yield_fixture
def server_process():
    process = Process(target=server.start_server)
    process.daemon = True
    process.start()
    yield process

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


def test_function(client_code):
    msg = "do you hear me at all?"

    try:
        client_code.sendall(msg)
        output = ""
        while True:
            part = client_code.recv(16)
            assert part
            output = output + part
            if len(part) < 16:
                client_code.shutdown(socket.SHUT_WR)
                client_code.close()
                break
        assert '<html>' in output
    except Exception as e:
        print e
<<<<<<< Updated upstream
=======
    assert output[-15:] == msg
    assert output[:15] == b"HTTP/1.1 200 OK"

# this should be run while no server is running
def test_response_error():
    
>>>>>>> Stashed changes
