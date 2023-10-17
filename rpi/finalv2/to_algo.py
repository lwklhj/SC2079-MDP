import socket
import threading
import time
import pickle

def myround(x,base=5):
  print('Entering my round',x)
  return base * round(x/base)

class algoInterface:
    def __init__(self, RPI):
        self.RPI = RPI
        self.clientSocket = socket.socket()
        self.status = 'stopped'
    
    def connectAlgo(self):
        self.clientSocket, self.address = self.RPI.serverSocket.accept()
        print("ALGO Connected on: ", self.address)
        #welcomeMessage = "Welcome to Server (ALGO)"
        #self.write(welcomeMessage)

        #start listen threads)
        listenThread = threading.Thread(target = self.read)
        listenThread.start()

    def write(self,message):
        try:
            message = message + '!'
            self.clientSocket.send(bytes(message,"utf-8"))
            # print("Sent to Algo: ", message)
        except Exception as e:
            print("Algo Disconnected! (ALGO WRITE)")
            self.connectAlgo()



    def read(self):
        while True:
            try:
                # 1024/5 commands
                message = self.clientSocket.recv(4096)
                commands = pickle.loads(message)
                print(commands)
                
                if (len(commands) > 0):
                    print("From ALGO:", commands)
                if (type(commands) is str):
                    data = commands.split("|")
                    #self.RPI.android.write(f"[TARGET, {data[1]}, {data[2]}]")
                else:
                    self.commands = commands
                    cThread = threading.Thread(target = self.commandsThread)
                    cThread.start()
                    # i = 0
                    # while(i < len(commands)):
                    #     command = commands[i]
                    #     print(command)
                    #     if(command[0] == 's'):
                    #         print("Send image")
                    #         self.RPI.android.write(f"[ROBOT, '{command}']")
                    #         result = self.RPI.imrec.take_picture(int(command[1:]))
                    #         # Send results to Android
                    #         #self.RPI.android.write(f"[TARGET, {int(command[1:])}, {result}]")
                    #     #elif(command[0] == 'U'):
                    #     #    print("Send android update command")
                    #     #    #self.RPI.android.write(command)
                    #     else:
                    #         self.RPI.stm.send(command)
                    #         try:
                    #             next_command = commands[i+1]
                    #             # Give coord to Android
                    #             self.RPI.android.write(f"[ROBOT, '{command}', '{next_command}']")
                    #             i += 1
                    #         except StopIteration:
                    #             break
                    #     i += 1


                # message = self.clientSocket.recv(1024)
                # message = message.decode()
                # if message:
                #     print("From ALGO:", message)
                # if ('Hello' not in message and 'AND' not in message and 'Update' not in message and 'NOTHING' not in message and 'conda' not in message):
                #     #message = message[4:]
                #     commands = message.split(',')
                #     convertedLetters = []
                #     for command in commands:
                #         print("commandEnter:",command)
                #         if (command == '0000'): continue
                #         if (command[2]!='0' and (command[3]=='0' or command[3]=='1')):
                #             print('Entering myround attempt')
                #             roundedValue = str(myround(int(command[2])))
                #             print('roundedVal:',roundedValue)
                #             if (roundedValue == '0'):
                #                 print('zero case detected')
                #                 pass
                #             elif roundedValue == '10':
                #                 convertedLetters.append(self.convertCommandToLetter('010'+command[3]))
                #             else: 
                #                 convertedLetters.append(self.convertCommandToLetter('005'+command[3]))
                #         convertedLetters.append(self.convertCommandToLetter(command))
                #     print("Full conversion: ", convertedLetters)
                #     i = 0
                #     for letter in convertedLetters:
                #         # Sending Commands to STM
                #         print('Sending to STM:', letter)
                #         self.RPI.stm.send(letter)

                #         # Sending commands to Android
                        
                #         messageToAndroid = "COMMAND FOUR DIGIT," + commands[i]
                #         self.RPI.android.write(messageToAndroid)
                #         i = i+1
                        

                #     #after full list of commands is sent, take a picture
                #     self.RPI.imrec.take_picture()

                # #Update Android with coordinates
                # elif("Update Android" in message):
                #     self.RPI.android.write(message)
                    
            except Exception as e:
                print("Algo Disconnected! (ALGO READ)")
                print(e)
                self.connectAlgo()

    def commandsThread(self):
        self.status = 'running'
        commands = self.commands
        i = 0
        while(i < len(commands)):
            command = commands[i]
            print(command)
            if(command[0] == 's'):
                print("Send image")
                #self.RPI.android.write(f"[ROBOT, '{command}']")
                self.RPI.imrec.take_picture(int(command[1:]))
            else:
                self.RPI.stm.send(command)
                try:
                    next_command = commands[i+1]
                    # Give coord to Android
                    #self.RPI.android.write(f"[ROBOT, '{command}', '{next_command}']")
                    i += 1
                except StopIteration:
                    break
            i += 1
        self.status = 'stopped'




    def convertCommandToLetter(self,command):
        print('command:',command)
        distance = int(command[0:3])
        direction = int(command[3])
        if (direction == 1 and distance == 5): return chr(ord('j')+11)
        if (direction == 0 and distance == 5): return chr(ord('9')+11)
                                                        
        if (direction == 0): charMap = ord('0')
        elif (direction == 1): charMap = ord('a')
        elif (direction == 2): return 'L'
        elif (direction == 3): return 'R'
        else:
            print('ERROR: Unknown direction mapping')
            return '?'
            
        letter = distance//10 + charMap - 1
        print(command,'->',letter,chr(letter))
            
        return chr(letter)

