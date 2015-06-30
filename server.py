import socket

ADDR = ('127.0.0.1', 8000)
socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
socket.bind(ADDR)
socket.listen(2)


def response_ok():
    return "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n"


def response_error():
    return "HTTP/1.1 500 not OK\r\nContent-Type: text/html; charset=utf-8\r\n"


<<<<<<< HEAD
def response_ok():
    return conn.sendall(
        "HTTP/1.1 200 OK\n"
        "Content-Type: text/html; charset=utf-8\n"
        "<!DOCTYPE html>\n"
        "<html>\n"
        "\t<head>\n"
        "\t\t<title>Status 200 OK</title>\n"
        "\t</head>\n"
        "\t<body>\n"
        "\t\t<p>HTTP:200 OK response</p>\n"
        "\t</body>\n"
        "</html>\n"
        )

while True:
    try:
        conn, addr = socket.accept()
        output = ""
        while True:
            msg = conn.recv(16)
            output = output + msg
            if len(msg) < 16:
                response_ok()
=======
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
            if "GET" in output:
                conn.sendall(response_ok())
>>>>>>> 7f8194aa87327d7cdcbf416a9bf612cf37666d32
                conn.sendall(output)
            else:
                conn.sendall(response_error())
            conn.close()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    return_request()

# arbitrary change
