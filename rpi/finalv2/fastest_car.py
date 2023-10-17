from ultrasonic import Ultrasonic
import time

class FastestCarTask:
    def __init__(self,RPI):
        self.RPI = RPI
        self.ultrasonic = Ultrasonic()
        self.commands = []
        self.distance_1 = 0
        self.distance_2 = 0
        
    def start(self):
        # Activate ultrasonic sensor

        while(self.ultrasonic.measure() > 40):
            self.RPI.stm.send("f0010")
            self.distance_1 += 10
            time.sleep(0.06)
        print(self.distance_1)
        self.RPI.imrec.take_picture(1)
        # Wait for commands from algo
        while(self.algo.status == 'stopped'):
            pass
        # Poll stm commands completion
        while(self.RPI.algo.status == 'running'):
            pass
        while(self.ultrasonic.measure() > 40):
            self.RPI.stm.send("f0010")
            self.distance_2 += 10
            time.sleep(0.06)
        print(self.distance_2)
        #self.enqueueCommand("l0020")
        #result = self.RPI.imrec.take_picture()

    def enqueueCommand(self, command):
        self.commands.push(command)

    def runAndWait(self):
        while(self.commands.count !=0 ):
            command = self.commands.pop()
            self.RPI.stm.send(command)