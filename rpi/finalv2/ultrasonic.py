import RPi.GPIO as GPIO
import time

class Ultrasonic:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.PIN_TRIGGER = 7
        self.PIN_ECHO = 11
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        
    def measure(self):
        GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(self.PIN_ECHO) == GPIO.low:
            start = time.time()
        while GPIO.input(self.PIN_ECHO) == GPIO.high:
            end = time.time()
            
        duration = end - start
        distance = (duration * 34000) / 2
        return distance