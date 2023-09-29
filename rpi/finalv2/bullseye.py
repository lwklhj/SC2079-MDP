class bullseyeInterface:
    def __init__(self,RPI):
        self.RPI = RPI
        self.commands = []

    def start(self):
        
        result = self.RPI.imrec.take_picture()
        count = 1

        while(result == "Back" and count!=4):
                self.RPI.stm.send("b0060")
                self.RPI.stm.send("r0090")
                self.RPI.stm.send("l0090")
                self.RPI.stm.send("l0090")
                result = self.RPI.imrec.take_picture()
                count = count + 1

# 'b0010', 'U65.0-105.0-E', 'b0010', 'U55.0-105.0-E', 
# 'b0010', 'U45.0-105.0-E', 'b0010', 'U35.0-105.0-E', 
# 'b0010', 'U25.0-105.0-E', 'b0010', 'U15.0-105.0-E', 
# 'r0090', 'U45.0-75.0-S', 'l0090', 'U75.0-45.0-E', 
# 'l0090', 'U105.0-75.0-N', 's0000'