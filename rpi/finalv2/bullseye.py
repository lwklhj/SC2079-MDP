class bullseyeInterface:
    def __init__(self,RPI):
        self.RPI = RPI
        self.commands = []

    def start(self):
        
        result = self.RPI.imrec.take_picture()
        count = 1

        while(result == "back" and count!=4):
                self.RPI.stm.send("b0030")
                self.RPI.stm.send("r0090")
                self.RPI.stm.send("f0010")
                self.RPI.stm.send("l0090")
                self.RPI.stm.send("l0090")
                result = self.RPI.imrec.take_picture()
                count = count + 1

