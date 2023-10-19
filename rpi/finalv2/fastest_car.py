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
        measured = int(self.ultrasonic.measure())
        while(measured > 40):
            if measured - 20 < 40:
              temp = measured - 40
              self.distance_1 += temp
              self.RPI.stm.send("f00" + str(temp))
              break
            else:
              self.RPI.stm.send("f0020")
              self.distance_1 += 20
              time.sleep(0.06)
              measured = int(self.ultrasonic.measure())
        print(self.distance_1)
        # Send distance to algo
        self.RPI.algo.write(f"dist1|{self.distance_1}")
        # Take picture
        self.RPI.imrec.take_picture(1)
        # Wait for commands from algo
        while(self.RPI.algo.status == 'stopped'):
            pass
        # Poll stm commands completion
        while(self.RPI.algo.status == 'running'):
            pass
        measured = int(self.ultrasonic.measure())
        while(measured > 40):
            if measured - 20 < 40:
              temp = measured - 40
              self.distance_2 += temp
              self.RPI.stm.send("f00" + str(temp))
              break
            else:
              self.RPI.stm.send("f0020")
              self.distance_2 += 20
              time.sleep(0.06)
              measured = int(self.ultrasonic.measure())
        print(self.distance_2)
        self.RPI.algo.write(f"dist2|{self.distance_2}")
        self.RPI.imrec.take_picture(2)
        while(self.algo.status == 'stopped'):
            pass
        # Poll stm commands completion
        while(self.RPI.algo.status == 'running'):
            pass
        #self.enqueueCommand("l0020")
        #result = self.RPI.imrec.take_picture()

    def enqueueCommand(self, command):
        self.commands.push(command)

    def runAndWait(self):
        while(self.commands.count !=0 ):
            command = self.commands.pop()
            self.RPI.stm.send(command)