import socket as s
import os
import mimetypes


ROOT_DIRECTORY = os.path.join(__file__, b'webroot/')


def response_ok(uri):
    length = str(len(resolve_uri(uri)[0]))
    response = b"HTTP/1.1 200 OK\r\nContent-Type: {}; charset=utf-8\
    \r\nContent-Length: {}\r\n\r\n {}".format(resolve_uri(uri)[1],
                                              length, resolve_uri(uri)[0])
    return response


def response_error(error_code, reason_phrase):
    response = b"HTTP/1.1 {} {}\r\nContent_Type: text/html;\
    charset=utf-8\r\n".format(error_code, reason_phrase)
    return response


def return_request():
    ADDR = ('127.0.0.1', 8000)
    socket = s.socket(
        s.AF_INET, s.SOCK_STREAM, s.IPPROTO_IP
    )

    socket.bind(ADDR)
    socket.listen(1)
    while True:
        try:
            conn, addr = socket.accept()
            request = ""
            while True:
                msg = conn.recv(1024)
                request = request + msg
                if len(msg) < 1024:
                    break
            try:
                response = response_ok(parse_request(request))
            except ValueError as detail:
                response = response_error(b"400", str(detail))
            except LookupError as detail:
                response = response_error(b"404", str(detail))
            except AttributeError as detail:
                response = response_error(b"405", str(detail))
            except NotImplementedError as detail:
                response = response_error(b"500", str(detail))
            except UserWarning as detail:
                response = response_error(b"403", str(detail))
            conn.sendall(response)
            conn.close()
        except KeyboardInterrupt:
            break


def parse_request(request):
    request = request.split("\r\n")
    if "GET " not in request[0][:4]:
        raise AttributeError("Error.  Must send GET request")
    if "HTTP/1.1" not in request[0][-8:]:
        raise NotImplementedError("Error. Only accepts HTTP 1.1 Protocol")
    host = [o for o in request if o[:6] == "Host:"]
    if host == []:
        raise ValueError("Error. Must provide host")
    else:
        first_line = request[0].split(" ")
        return first_line[1]


def resolve_uri(uri):
    uri = os.path.join(ROOT_DIRECTORY + uri.strip(b"/"))
    if b".." in uri:
        raise UserWarning(b"Permission denied")
    if os.path.isfile(uri):
        with open(uri) as resource:
            body = resource.read()
            content_type = mimetypes.guess_type(resource)[0]
    elif os.path.isdir(uri):
        content_type = b"text/html"
        body = b"<!DOCTYPE html>\n<html> "
        for item in os.listdir(uri):
            body += b"\t\t<li> {} </li>".format(item)
        body = b"\t<ul> {} \t</ul>\n</html>".format(body)
    else:
        raise LookupError(b"Resource not found.")

    return (body, content_type)


if __name__ == "__main__":
    return_request()
