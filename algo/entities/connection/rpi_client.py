import pickle
import socket


class RPiClient:
    """
    Used for connecting to...
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send_message(self, obj):
        print("sending")
        self.socket.sendall(pickle.dumps(obj))
        print("Sent")

    def close(self):
        self.socket.close()
