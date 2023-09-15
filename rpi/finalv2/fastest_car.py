class FastestCarTask:
    def __init__(self,RPI):
        self.RPI = RPI
        self.commands = []
        
    def start(self):
        # Activate ultrasonic sensor
        self.enqueueCommand("uuuuu")
        self.enqueueCommand("l0020")
        result = self.RPI.imrec.take_picture()
        if(result == "left"):
            self.RPI.stm.send("l0090")
            self.RPI.stm.send("r0090")
            self.RPI.stm.send("r0090")
            self.RPI.stm.send("l0090")
        else:
            self.RPI.stm.send("r0090")
            self.RPI.stm.send("l0090")
            self.RPI.stm.send("l0090")
            self.RPI.stm.send("r0090")

        self.RPI.stm.send("l0020")

    def enqueueCommand(self, command):
        self.commands.push(command)

    def runAndWait(self):
        while(self.commands.count !=0 ):
            command = self.commands.pop()
            self.RPI.stm.send(command)