import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 4851))
sock.listen(5)

while True:
    try:
        client, addr = sock.accept()
        print(client, "\n", addr[0]) # выведет инфо о клиенте
    except KeyboardInterrupt:
        print("ERR")
        sock.close()
        break
    else:
        result = client.recv(1024)
        client.send(b"Done!")
        client.close()
        print("Message: ", result.decode("utf-8"))