import socket as s
import os


ROOT_DIRECTORY = b'webroot/'


def response_ok(uri):
    length = str(len(resolve_uri(uri)[0]))
    response = b"HTTP/1.1 200 %s\r\nContent-Type: %s; charset=utf-8\
    \r\nContent-Length: %s\r\n\r\n %s" % (uri, resolve_uri(uri)[1],
                                          length, resolve_uri(uri)[0])
    return response


def response_error(error_code, reason_phrase):
    response = "HTTP/1.1 " + error_code + " " + reason_phrase + "\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
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
                uri = parse_request(request)
                conn.sendall(response_ok(uri))
            except ValueError as detail:
                detail = str(detail)
                conn.sendall(response_error("400", detail))
            except LookupError as detail:
                detail = str(detail)
                conn.sendall(response_error("404", detail))
            except AttributeError as detail:
                detail = str(detail)
                conn.sendall(response_error("405", detail))
            except NotImplementedError as detail:
                detail = str(detail)
                conn.sendall(response_error("500", detail))
            conn.close()
        except KeyboardInterrupt:
            break


def parse_request(request):
    if "GET" not in request:
        raise AttributeError("Error.  Must send GET request")
    if "HTTP/1.1" not in request:
        raise NotImplementedError("Error. Only accepts HTTP 1.1 Protocol")
    if "Host:" not in request:
        raise ValueError("Error. Must provide host")
    else:
        request_lines = request.split(b"\r\n")
        first_line = request_lines[0].split(" ")
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
                body += "\t\t<li>" + item + "</li>"
            body = "\t<ul>" + body + "\t</ul>\n</html>"
    except:
        raise LookupError("Resource not found.")

    return (body, content_type)


if __name__ == "__main__":
    return_request()
