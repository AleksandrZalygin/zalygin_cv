import numpy as np
import matplotlib.pyplot as plt
import socket

SERVER_IP = "84.237.21.36"
SERVER_PORT = 5152


def get_neighbours(y, x):
    neighbours = [
        (y - 1, x), (y - 1, x - 1), (y - 1, x + 1),
        (y + 1, x + 1), (y + 1, x),
        (y, x - 1), (y, x + 1), (y + 1, x - 1)
    ]
    return neighbours


def is_local_max(arr, y, x):
    for ny, nx in get_neighbours(y, x):
        if arr[y, x] <= arr[ny, nx]:
            return False
    return True


def receive_data(sock, size):
    buffer = bytearray()
    while len(buffer) < size:
        packet = sock.recv(size - len(buffer))
        if not packet:
            return None
        buffer.extend(packet)
    return buffer


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((SERVER_IP, SERVER_PORT))

    for _ in range(10):
        sock.send(b"get")

        data = receive_data(sock, 40002)
        if data is None:
            break

        img_height, img_width = data[0], data[1]
        image = np.frombuffer(data[2:], dtype=np.uint8).reshape(img_height, img_width)

        local_maxima = [
            (y, x) for y in range(img_height) for x in range(img_width)
            if is_local_max(image, y, x)
        ]

        if len(local_maxima) >= 2:
            dist = np.linalg.norm(
                np.array(local_maxima[0]) - np.array(local_maxima[1])
            )
            sock.send(f"{dist:.1f}".encode())
        else:
            sock.send(b"0.0")

        response = sock.recv(20)
        print(response.decode().strip())

    sock.send(b"beat")
    heartbeat_response = sock.recv(20)
    print(heartbeat_response.decode().strip())
