import socket as s
import os


ROOT_DIRECTORY = b'webroot/'


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
                response = response_error("400", str(detail))
            except LookupError as detail:
                response = response_error("404", str(detail))
            except AttributeError as detail:
                response = response_error("405", str(detail))
            except NotImplementedError as detail:
                response = response_error("500", str(detail))
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
    uri = ROOT_DIRECTORY + uri
    try:
        if b"." in uri:
            body = open(uri).read()
            if b".html" in uri:
                content_type = b"text/html"
            elif b".jpg" in uri:
                content_type = b"image/jpg"
            elif b".png" in uri:
                content_type = b"image/png"
            else:
                content_type = b"text/plain"
        else:
            content_type = b"text/html"
            body = "<!DOCTYPE html>\n<html> "
            for item in os.listdir(uri):
                body += "\t\t<li> {} </li>".format(item)
            body = "\t<ul> {} \t</ul>\n</html>".format(body)
    except:
        raise LookupError("Resource not found.")

    return (body, content_type)


if __name__ == "__main__":
    return_request()
