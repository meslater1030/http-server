import socket
import sys

ADDR = ('127.0.0.1', 8000)
client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )


def response_error():
    return sys.stdout.write(
        "HTTP/1.1 500 not OK\n"
        "Content-Type: text/html; charset=utf-8\n"
        "<!DOCTYPE html>\n"
        "<html>\n"
        "\t<head>\n"
        "\t\t<title>Status 500 not OK</title>\n"
        "\t</head>\n"
        "\t<body>\n"
        "\t\t<p>HTTP:500 Internal Server Error</p>\n"
        "\t</body>\n"
        "</html>\n"
        )

try:
    client.connect(ADDR)
except Exception as e:
    response_error()

msg = "do you hear anything?"

try:
    client.sendall(msg)
    output = ""
    while True:
        part = client.recv(16)
        output = output + part
        if len(part) < 16:
            sys.stdout.write(output)
            client.shutdown(socket.SHUT_WR)
            client.close()
            break
except Exception as e:
    print e
