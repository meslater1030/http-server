#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import socket
from server import response_ok, parse_request, resolve_uri


def test_response_ok():
    response = response_ok(b"this is from the client")
    assert b"200" in response


@pytest.fixture()
def client_code():
    ADDR = ('127.0.0.1', 8000)
    client_conn = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

    client_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_conn.connect(ADDR)
    return client_conn


def test_functional(client_code):
    msg = b"GET /index.html HTTP/1.1\r\nHost:"

    try:
        client_code.sendall(msg)
        output = ""
        while True:
            part = client_code.recv(1024)
            assert part
            output = output + part
            if len(part) < 1024:
                client_code.shutdown(socket.SHUT_WR)
                client_code.close()
                break
    except Exception as e:
        print e
    assert b'200' in output


def test_bad_request_functional(client_code):
    msg = "do you hear me at all?"

    try:
        client_code.sendall(msg)
        output = b""
        while True:
            part = client_code.recv(1024)
            assert part
            output = output + part
            if len(part) < 1024:
                client_code.shutdown(socket.SHUT_WR)
                client_code.close()
                break
    except Exception as e:
        print e
    assert b"400" in output


def test_bad_parse():
    bad_request = b"some_bad_request"
    with pytest.raises(ValueError):
        parse_request(bad_request)


def test_parse_request():
    bad_request = b"GET /index.html HTTP/1.1\r\nHost:"
    response = parse_request(bad_request)
    assert b"/index.html" in response


def test_root():
    request = b"GET sample.txt HTTP/1.1\r\nHost:"
    uri = parse_request(request)
    response = resolve_uri(uri)
    assert b"This is a very simple text file" in response[0]
