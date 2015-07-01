#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import socket
from server import response_ok, response_error


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
    except Exception as e:
        print e
    assert '<html>' in output
    assert '200' in output
    assert 'do you hear me at all?' in output


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
