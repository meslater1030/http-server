import socket
import sys

ADDR = ('127.0.0.1', 8000)
client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
client.connect(ADDR)

<<<<<<< HEAD
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
=======

def send_request(msg):
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

if __name__ == "__main__":
    send_request("do you hear me?")
>>>>>>> 7f8194aa87327d7cdcbf416a9bf612cf37666d32
