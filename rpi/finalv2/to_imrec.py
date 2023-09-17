#import cv2
#import imagezmq
import socket
import threading
from picamera2 import Picamera2
import tensorflow as tf
import numpy as np

class imrecInterface:
    def __init__(self, RPI):
        self.RPI = RPI
        # self.clientSocket = socket.socket()
        # self.sender = None
        # self.attempts = 0
        TF_MODEL_FILE_PATH = 'model.tflite' # The default path to the saved TensorFlow Lite model
        self.interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
        self.picam2 = Picamera2()
        config = self.picam2.still_configuration(main={"size": (180, 180), "format": "BGR888"})
        self.picam2.configure(config)
    
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
        # sender = imagezmq.ImageSender(connect_to='tcp://192.168.20.25:5555')
        # cam = cv2.VideoCapture(0)
        # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # rpi_name = socket.gethostname()
        # check, image = cam.read()
        # try:
        #     sender.send_image(rpi_name, image)
        #     print("Image sent to IMREC server!")
        # except Exception as e:
        #     print("Image sending failed!")
        
        class_names = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40']

        self.picam2.start()
        img = self.picam2.capture_image("main")

        # Image size
        # img_height = 180
        # img_width = 180

        #img = tf.keras.utils.load_img(
        #    image_path, target_size=(img_height, img_width)
        #)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        classify_lite = self.interpreter.get_signature_runner('serving_default')

        predictions_lite = classify_lite(rescaling_3_input=img_array)['dense_4']
        score_lite = tf.nn.softmax(predictions_lite)

        # print(
        #     "This image most likely belongs to {} with a {:.2f} percent confidence."
        #     .format(class_names[np.argmax(score_lite)], 100 * np.max(score_lite))

        print(class_names[np.argmax(score_lite)])
        return class_names[np.argmax(score_lite)]