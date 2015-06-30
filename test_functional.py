#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import socket
from multiprocessing import Process
from server import response_ok, response_error


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
    response = response_ok()
    assert "200" in response


def test_response_error():
    response = response_error()
    assert "500" in response


@pytest.fixture()
def client_code():
    ADDR = ('127.0.0.1', 8000)
    client_conn = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

    client_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_conn.connect(ADDR)
    return client_conn


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
        assert '200' in output
        assert 'do you hear me at all?' in output
    except Exception as e:
        print e


def test_send_msg(client_code):
    client_code.sendall(b"GET Hello World")
    output = ""
    while True:
        part = client_code.recv(16)
        output = output + part
        if len(part) < 16:
            client_code.shutdown(socket.SHUT_WR)
            client_code.close()
            break
    assert b"World" in output
