import serial
import time

class STMInterface:
    def __init__(self,RPI):
        self.RPI = RPI
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
            print("Connected to STM via USB 0")
        except:
            try:
                self.ser = serial.Serial('/dev/ttyUSB1', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=3)
                print("Connected to STM via USB 1")
            except Exception as e2:
                print("Failed to connect to STM")
    def send(self,cmd):
        # Testing purpose
        cmd = list(cmd)
        """if cmd[0] == "f":
            cmd[0] = 'S'
            cmd[1] = 'F'
        elif cmd[0] == "b":
            cmd[0] = 'S'
            cmd[1] = 'B'
        elif cmd[0] == "L":
            cmd[0] = 'L'
            cmd[1] = 'B'
        elif cmd[0] == "l":
            cmd[0] = 'L'
            cmd[1] = 'F'
        elif cmd[0] == "R":
            cmd[0] = 'R'
            cmd[1] = 'B'
        elif cmd[0] == "r":
            cmd[0] = 'R'
            cmd[1] = 'F'"""
        flag = 0;
        if cmd[0] == "f":
            cmd[0] = 'F'
            cmd[1] = 'W'
        elif cmd[0] == "b":
            cmd[0] = 'B'
            cmd[1] = 'W'
        elif cmd[0] == "L":
            cmd[0] = 'B'
            cmd[1] = 'L'
            flag = 1
        elif cmd[0] == "l":
            cmd[0] = 'F'
            cmd[1] = 'L'
            flag = 1
        elif cmd[0] == "R":
            cmd[0] = 'B'
            cmd[1] = 'R'
            flag = 1
        elif cmd[0] == "r":
            cmd[0] = 'F'
            cmd[1] = 'R'
            flag = 1

        if (flag == 0):
            cmd_num = int("".join(cmd[2:]))
            print("This is the cmd_numb:", cmd_num)
            cmd_header = "".join(cmd[0:2])
            print("this is the cmd_header:", cmd_header)
            cmd = cmd_header + str(cmd_num).rjust(2, "0")
            cmd=cmd.lstrip()
        else:
            cmd_header = "".join(cmd[0:2])
            cmd = cmd_header+"00"
            cmd=cmd.lstrip()
            print("cd_header for fr/fl/br/bl"+cmd)

        #cmd = "".join(cmd)
        print(f"Sending Commands to STM: {cmd}")
        print(cmd) 
        self.ser.write((cmd+'\r').encode())
        print("I have sent over to STM")
        self.ser.flushInput()
        print(len(cmd))
        # Our STM sends two KKs , one when receive command, one when command fully excecuted
        while True:
            try:
                #s = self.ser.read(6).decode().rstrip().lstrip()
                s = self.ser.readline().decode.rstrip().lstrip()
                print("help me")
                #if(s[0:3] == "ACK"):
                if("ACK" in s):
                    break
                # Try to send the IR distance travelled to algo
                else:
                    distance = s.split("|")[0]
                    self.RPI.algo.write(f"IR|{distance}")

                    
            except:
                print("Failed to send command to STM!")
                break

#stmTest = STMInterface()
#stmTest.send('L')
