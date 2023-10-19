import os
import bluetooth
import threading
from to_algo import *
from to_imrec import *
from to_android import *
from to_stm import *
from bullseye import *
from testfile import *
import socket
from ultrasonic import *
from fastest_car import FastestCarTask


class RPI:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', 1234))
        self.serverSocket.listen(10)
        # initialise STM
        self.stm = STMInterface(self)

        # Initialise Android Interface
        self.android = androidInterface(self)

        # initialise algo interface
        self.algo = algoInterface(self)

        # initialise imrec interface
        self.imrec = imrecInterface(self)

        # initialise bullseye
        self.bullseye = bullseyeInterface(self)

        # initialise test
        self.testfile = testInterface(self)

        self.fastcar = FastestCarTask(self)

    def connect(self):
        threading.Thread(target=self.android.connectAndroid).start()
        threading.Thread(target=self.algo.connectAlgo).start()


        # self.imrec.connectImrec()
rpi = RPI()
rpi.connect()
# rpi.bullseye.start()
# rpi.imrec.take_picture()
rpi.testfile.start()
#fastCarTask = FastestCarTask(rpi)
#fastCarTask.start()
