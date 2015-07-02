#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import socket
from server import response_ok, parse_request, resolve_uri


@pytest.fixture()
def client_code():
    ADDR = ('127.0.0.1', 8000)
    client_conn = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

    client_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_conn.connect(ADDR)
    return client_conn


def test_response_ok():
    response = response_ok('a_web_page.html')
    assert "200" in response


def test_bad_HTTP():
    bad_request = b"GET a_web_page.html HTTP/1.0\r\nHost:"
    with pytest.raises(NotImplementedError):
        parse_request(bad_request)


def test_no_GET():
    no_GET = b"a_web_page.html HTTP/1.1\r\nHost:"
    with pytest.raises(AttributeError):
        parse_request(no_GET)


def test_no_host():
    no_host = b"GET a_web_page.html HTTP/1.1\r\n"
    with pytest.raises(ValueError):
        parse_request(no_host)


def test_not_found():
    not_found = b"GET starbucks.html HTTP/1.1\r\nHost:"
    with pytest.raises(LookupError):
        resolve_uri(parse_request(not_found))


def test_parse_request():
    bad_request = b"GET a_web_page.html HTTP/1.1\r\nHost:"
    response = parse_request(bad_request)
    assert b"a_web_page.html" in response


def test_uri_response():
    request = b"GET sample.txt HTTP/1.1\r\nHost:"
    uri = parse_request(request)
    response = resolve_uri(uri)
    assert b"This is a very simple text file" in response[0]
    assert b"text" in response[1]


def test_uri_dir():
    request = b"GET images HTTP/1.1\r\nHost:"
    uri = parse_request(request)
    response = resolve_uri(uri)
    assert b"JPEG" in response[0]


def test_length():
    request = b"GET sample.txt HTTP/1.1\r\nHost:"
    uri = parse_request(request)
    response = response_ok(uri)
    assert "Content-Length: 96" in response


def bad_parse():
    request = b"""GETTER sample.txt HTTP/1.11\r\n
    Content-Type: noodles\r\nHoster: bathtime"""
    with pytest.raises(AttributeError):
        resolve_uri(request)
