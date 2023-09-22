import serial
import time

class STMInterface:
    def __init__(self,RPI):
        self.RPI = RPI
        return
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=3)
            print("Connected to STM via USB 0")
        except:
            try:
                self.ser = serial.Serial('/dev/ttyUSB1', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=3)
                print("Connected to STM via USB 1")
            except Exception as e2:
                print("Failed to connect to STM")
    def send(self,cmd):
        # Testing purpose
    
        print(f"Sending Commands to STM: {cmd}")

        if(not cmd[0].isdigit()):
            opcode = cmd[0]
            operands = cmd[1:]
            match opcode:
                case "l":
                    converted_opcode = "02"
                case 'r':
                    converted_opcode = "03"
                case "L":
                    converted_opcode = "12"
                case 'R':
                    converted_opcode = "13"
                case "f":
                    converted_opcode = "01"
                case 'b':
                    converted_opcode = "11"

            sc = converted_opcode + operands
            sc = str.encode(cmd)

        self.ser.write(sc)
        self.ser.flushInput()
        
        # Our STM sends two KKs , one when receive command, one when command fully excecuted
        first_k = False
        while True:
            try:
                s = self.ser.read().rstrip()
                s = s.lstrip()
                if s.decode() == 'K':
                    if(first_k):
                        print(s.decode())
                        break
                    first_k = True
            except:
                print("Failed to send command to STM!")
                break

#stmTest = STMInterface()
#stmTest.send('L')
