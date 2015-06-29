import socket

ADDR = ('127.0.0.1', 8000)
client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

client.connect(ADDR)

msg = "do you hear me at all?"

try:
    client.sendall(msg)
    output = ""
    while True:
        part = client.recv(16)
        output = output + part
        client.shutdown(socket.SHUT_WR)
        if len(part) < 16:
            print output
            client.close()
            break
except Exception as e:
    print e
