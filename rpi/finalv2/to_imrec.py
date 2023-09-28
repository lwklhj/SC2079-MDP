#import cv2
#import imagezmq
import socket
import threading
from picamera2 import Picamera2
from ultralytics import YOLO
from PIL import Image
import numpy as np
import os

class imrecInterface:
    def __init__(self, RPI):
        self.RPI = RPI
        # self.clientSocket = socket.socket()
        # self.sender = None
        # self.attempts = 0
        TF_MODEL_FILE_PATH = 'yolov8n.pt' # The default path to the saved TensorFlow Lite model
        self.model = YOLO(TF_MODEL_FILE_PATH)
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration(main={"size": (640, 640), "format": "BGR888"})
        self.picam2.configure(config)
        self.i = 0
    
    # Defunct
    def connectImrec(self):
        # self.clientSocket, self.address = self.RPI.serverSocket.accept()
        # print("IMREC Connected on: ", self.address)
        # welcomeMessage = "Welcome to Server (IMREC)"
        # self.write(welcomeMessage)
        # listenThread = threading.Thread(target = self.read)
        # listenThread.start()
        # self.sender = imagezmq.ImageSender(connect_to='tcp://192.168.20.25:5555')
        return
    
    # Defunct
    def read(self):
        # while True:
        #     try:
        #         message = self.clientSocket.recv(1024)
        #         message = message.decode('utf-8')

        #         if message:
        #             print("From IMREC:",message)
        #             # Send the image result to both android and algo
        #             if message == "NOTHING" and self.attempts < 4:
        #                 print("Executing failure attempt: ", str(self.attempts))
        #                 self.RPI.stm.send('a')
        #                 self.take_picture()
        #                 self.attempts= self.attempts + 1
                        
        #             else:
        #                 while self.attempts > 0:
        #                     self.RPI.stm.send('0')
        #                     self.attempts = self.attempts -1
                        
        #                 print("Attempts remaining:", self.attempts)
                        
        #                 messageToAndroid = 'TARGET,' + str(1) +',' + message
        #                 self.RPI.android.write(messageToAndroid)
        #                 self.RPI.algo.write(message)
                        
        #     except Exception as e:
        #         print("IMREC Disconnected! (imrec READ)")
        #         self.connectImrec()
        return
    # def write(self,message):
    #     self.clientSocket.send(message.encode())
            
            

    def take_picture(self):        
        class_names = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40']

        self.picam2.start()
        img = self.picam2.capture_array("main")
        results = self.model.predict(img, save = True, imgsz=640, conf=0.5, save_txt=True, save_conf=True)

        print(results[0].save_dir)
        # for file in os.listdir(results[0].save_dir+'/labels'):
        #     if file.endswith('.txt'):
        #         print(file)
        #         with open(r.save_dir+'/labels/'+file, 'r') as f:
        #             lines = f.readlines()
        #             if lines:
        #                 first_integer = int(lines[0].split()[0])
        #                 print("Detected image:", classes[first_integer])
        #             else:
        #                 print("No lines in file:", file)

        # print(class_names[np.argmax(score_lite)])
        # return class_names[np.argmax(score_lite)]
        return 0