#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import socket
from server import response_ok, response_error, parse_request


def test_response_ok():
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


@pytest.fixture()
def bad_client_code():
    ADDR = ('127.0.0.1', 8001)
    client_conn = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

    client_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_conn.connect(ADDR)
    return client_conn


def test_functional(client_code):
    msg = "do you hear me at all?"

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
    assert '<html>' in output
    assert '200' in output
    assert 'do you hear me at all?' in output


def test_bad_functional(bad_client_code):
    msg = "do you hear me at all?"

    try:
        bad_client_code.sendall(msg)
        output = ""
        while True:
            part = bad_client_code.recv(1024)
            assert part
            output = output + part
            if len(part) < 1024:
                bad_client_code.shutdown(socket.SHUT_WR)
                bad_client_code.close()
                break
    except Exception as e:
        print e
    assert "500" in response


def test_bad_parse():
    bad_request = b"some_bad_request"
    response = parse_request(bad_request)
    assert b"400: Bad Request" in response
    assert b""


def test_parse_request():
    bad_request = b"good request"
    response = parse_request(bad_request)
    assert b"200" in response
