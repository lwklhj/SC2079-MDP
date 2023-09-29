class testInterface:
    def __init__(self, RPI):
        self.RPI = RPI

    def start(self):
        self.RPI.stm.send("r0090")
