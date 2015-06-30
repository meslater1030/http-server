import socket

ADDR = ('127.0.0.1', 8000)
socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

socket.bind(ADDR)

socket.listen(1)


while True:
    try:
        conn, addr = socket.accept()
        output = ""
        while True:
            msg = conn.recv(16)
            output = output + msg
            if len(msg) < 16:
                conn.sendall(output)
                conn.close()
                break
    except KeyboardInterrupt:
        break
