#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Concurrent server using gevent
"""

import server
from gevent import socket as g


def return_concurrent_request():
    ADDR = ('127.0.0.1', 8000)
    socket = g.socket(
        g.AF_INET, g.SOCK_STREAM, g.IPPROTO_IP
    )

    socket.bind(ADDR)
    socket.listen(5)
    while True:
        try:
            conn, addr = socket.accept()
            request = ""
            while True:
                msg = conn.recv(1024)
                request += msg
                if len(msg) < 1024:
                    break
            try:
                response = server.response_ok(server.parse_request(request))
            except ValueError as detail:
                response = server.response_error(b"400", str(detail))
            except LookupError as detail:
                response = server.response_error(b"404", str(detail))
            except AttributeError as detail:
                response = server.response_error(b"405", str(detail))
            except NotImplementedError as detail:
                response = server.response_error(b"400", str(detail))
            except UserWarning as detail:
                response = server.response_error(b"403", str(detail))
            conn.sendall(response)
            conn.close()
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    return_concurrent_request()
