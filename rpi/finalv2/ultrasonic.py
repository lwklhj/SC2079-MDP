import RPi.GPIO as GPIO
import time

class Ultrasonic:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.PIN_TRIGGER = 16
        self.PIN_ECHO = 18
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        
    def measure(self):
        GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(self.PIN_ECHO) == GPIO.LOW:
            start = time.time()
        while GPIO.input(self.PIN_ECHO) == GPIO.HIGH:
            end = time.time()
            
        duration = end - start
        distance = (duration * 34000) / 2
        print("Measured Distance: ", distance)
        return distance