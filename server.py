import socket

ADDR = ('127.0.0.1', 8000)
socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
socket.bind(ADDR)
socket.listen(2)


def response_ok(reason_phrase):
    return "HTTP/1.1 200" + reason_phrase + "\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"


def response_error(error_code, reason_phrase):
    response = "HTTP/1.1 " + error_code + " " + reason_phrase + "\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    return response


def return_request():
    while True:
        try:
            conn, addr = socket.accept()
            output = ""
            while True:
                msg = conn.recv(16)
                output = output + msg
                if len(msg) < 16:
                    break
            try:
                final = parse_request(output)
                conn.sendall(response_ok(final))
            except ValueError as detail:
                detail = str(detail)
                conn.sendall(response_error("400", detail))
            conn.close()
        except KeyboardInterrupt:
            break


def parse_request(request):
    if "GET" not in request:
        raise ValueError("Error.  Must send GET request")
    if "HTTP/1.1" not in request:
        raise ValueError("Error. Only accepts HTTP 1.1 Protocol")
    if "Host:" not in request:
        raise ValueError("Error. Must provide host")
    else:
        request_lines = request.split(b"\r\n")
        first_line = request_lines[0].split(" ")
        return first_line[1]


if __name__ == "__main__":
    return_request()
<<<<<<< HEAD

# arbitrary change
=======
>>>>>>> 95c13df0a22891e7ff5f38a93dbd9fec405fe184
