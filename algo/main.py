import sys
import time
import pickle
from typing import List

import image_join
import settings
from app import AlgoSimulator, AlgoMinimal
from entities.assets.direction import Direction
from entities.connection.rpi_client import RPiClient
from entities.connection.rpi_server import RPiServer
from entities.grid.obstacle import Obstacle
from ultralytics import YOLO
import base64
import threading
import os


def parse_obstacle_data(data) -> List[Obstacle]:
    obs = []
    for obstacle_params in data:
        obs.append(Obstacle(obstacle_params[0],
                            obstacle_params[1],
                            Direction(obstacle_params[2]),
                            obstacle_params[3]))
    # [[x, y, orient, index], [x, y, orient, index]]
    print("Parsed obstacles:")
    for i in obs:
        print(i)
    return obs


def run_simulator():
    # Fill in obstacle positions with respect to lower bottom left corner.
    # (x-coordinate, y-coordinate, Direction)
    obstacles = [[65, 45, 180, 0], [15, 125, -90, 1], [115, 95, 180, 2],
                 [165, 55, 90, 3], [145, 145, -90, 4], [85, 175, 0, 5], [45, 185, -90, 6], [125, 5, 90, 7]]
    # obstacles = [[175, 55, -90, 0], [175, 95, 90, 1],
    #              [175, 85, 180, 2], [15, 195, -90, 3], [15, 55, 0, 4]]
    obs = parse_obstacle_data(obstacles)
    app = AlgoSimulator(obs)
    app.init()
    app.execute()
    app.robot.convert_all_commands()


def run_minimal(also_run_simulator):
    # Create a client to connect to the RPi.
    print(f"Attempting to connect to {settings.RPI_HOST}:{settings.RPI_PORT}")
    client = RPiClient(settings.RPI_HOST, settings.RPI_PORT)
    # Wait to connect to RPi.
    while True:
        try:
            client.connect()
            break
        except OSError:
            pass
        except KeyboardInterrupt:
            client.close()
            sys.exit(1)
    print("Connected to RPi!\n")

    print("Waiting to receive obstacle data from RPi...")
    # # Create a server to receive information from the RPi.
    # server = RPiServer(settings.PC_HOST, settings.PC_PORT)
    # # Wait for the RPi to connect to the PC.
    # try:
    #     server.start()
    # except OSError or KeyboardInterrupt as e:
    #     print(e)
    #     server.close()
    #     client.close()
    #     sys.exit(1)

    # At this point, both the RPi and the PC are connected to each other.
    # Create a synchronous call to wait for RPi data.

    # obstacle_data: list = server.receive_data()
    # server.close()

    buffer = []
    count_scans = 0
    while True:
        received = client.socket.recv(64768000)  # 4096 is the buffer size
        buffer.append(received)
        # Join bytes into byte string
        data = b''.join(buffer)
        data = data.decode()
        # No more incoming bytes
        # Start operations
        if "!" in data:
            # Reset buffer
            buffer.clear()
            data = data.replace("!", "")
            print(type(data))
            # print(data)
            if (data.split('|')[0] == "img"):
                try:
                    
                    print("1st")
                    index = data.split('|')[1]
                    print("2nd")
                    image_data_base64 = data.split('|')[2]

                    print(len(image_data_base64))

                    image_data_base64 = image_data_base64[2:len(
                        image_data_base64)-1]

                    # buffer needed for multiple of 4
                    # buffer_needed = 4 -((len(image_data_base64)) %4)
                    # image_data_base64 += '=' * buffer_needed

                    print(image_data_base64[:50])
                    print(image_data_base64[-50:])
                    print(len(image_data_base64))
                    print(type(image_data_base64))

                    img = pickle.loads(base64.b64decode(image_data_base64))
                    print("3rd")
                    # Load Model
                    MODEL_FILE_PATH = '/Users/jordan/Documents/Github/SC2079-MDP/algo/best1.pt'
                    model = YOLO(MODEL_FILE_PATH)
                    folder_path = "/Users/jordan/Documents/Github/SC2079-MDP/algo/predictions"
                    # Start imrec
                    results = model.predict(img, save=True, imgsz=640, conf=0.5, save_txt=True,
                                            save_conf=True, project=folder_path)
                    classes = results[0].names
                    first_integer = -1
                    for file in os.listdir(results[0].save_dir+'/labels'):
                        if file.endswith('.txt'):
                            with open(results[0].save_dir+'/labels/'+file, 'r') as f:
                                lines = f.readlines()
                                if lines:
                                    if len(lines) != 1:
                                        first_line = 0
                                        first_integer = int(lines[first_line].split()[0])
                                        while(first_integer == 30):
                                            first_line += 1
                                            first_integer = int(lines[first_line].split()[0])
                                    else:
                                        first_integer = int(lines[0].split()[0])
                                    print(first_integer)
                                    print("Detected image:",
                                        classes[first_integer])
                    count_scans += 1
                    if(len(obstacles)==count_scans):
                        image_join.collate_images(folder_path)
                    
                    if first_integer != -1:  
                        # Send result back
                        response = f"imgID|{index}|{classes[first_integer]}"
                        # if (len(data.split("|") == 4)):
                        #     response += f"|{data.split('|')[3]}"
                        print("Sending response: ", response)
                        client.send_message(response)
                        print("Sent response")
                    
                except Exception as e:
                    print("IMAGE RECOGNITION ERROR: ", e)

            else:
                data = data.split(',')  # Split on delimiter

                obstacle_data = []  # Array for storing obstacle data

                i = 0
                while (i < len(data)):
                    # Android formatted the data as below
                    # Ori,x,y,no,ori2,x2,y2,no2
                    obstacle_data.append(
                        (int(data[i]), int(data[i+1]), int(data[i+2]), int(data[i+3])))
                    i += 4  # Every four strings is an obstacle
                obstacles = parse_obstacle_data(obstacle_data)

                if also_run_simulator:
                    app = AlgoSimulator(obstacles)
                    app.init()
                    threading.Thread(target=app.execute).start()

                app = AlgoMinimal(obstacles)
                app.init()
                app.execute()

                # Send the list of commands over.
                print("Sending list of commands to RPi...")
                commands = app.robot.convert_all_commands()
                client.send_message(commands)

        # data = data.decode()  # convert to string

        # print("Got data from RPi:")
        # # print(data)
        # # Check if image
        # if (data.split('|')[0] == "img"):
        #     try:
        #         index = data.split('|')[0][4:-1]
        #         img = pickle.loads(base64.b64decode(data.split(':')[1]))
        #         # Load Model
        #         MODEL_FILE_PATH = 'best.pt'
        #         model = YOLO(MODEL_FILE_PATH)
        #         # Start imrec
        #         results = model.predict(img, save=True, imgsz=640, conf=0.5, save_txt=True,
        #                                 save_conf=True, project="/Users/jordan/Documents/Github/SC2079-MDP/algo")
        #         classes = results[0].names
        #         for file in os.listdir(results[0].save_dir+'/labels'):
        #             if file.endswith('.txt'):
        #                 with open(results[0].save_dir+'/labels/'+file, 'r') as f:
        #                     lines = f.readlines()
        #                     if lines:
        #                         first_integer = int(lines[0].split()[0])
        #                         print("Detected image:",
        #                               classes[first_integer])
        #         # Send result back
        #         client.send_message(f"imgID|{index}|{classes[first_integer]}")
        #     except Exception as e:
        #         print("IMAGE RECOGNITION ERROR: ", e)

        # else:
        #     data = data.split(',')  # Split on delimiter

        #     obstacle_data = []  # Array for storing obstacle data

        #     i = 0
        #     while (i < len(data)):
        #         # Android formatted the data as below
        #         # Ori,x,y,no,ori2,x2,y2,no2
        #         obstacle_data.append(
        #             (int(data[i]), int(data[i+1]), int(data[i+2]), int(data[i+3])))
        #         i += 4  # Every four strings is an obstacle
        #     obstacles = parse_obstacle_data(obstacle_data)

        #     if also_run_simulator:
        #         app = AlgoSimulator(obstacles)
        #         app.init()
        #         threading.Thread(target=app.execute).start()

        #     app = AlgoMinimal(obstacles)
        #     app.init()
        #     app.execute()

        #     # Send the list of commands over.
        #     print("Sending list of commands to RPi...")
        #     commands = app.robot.convert_all_commands()
        #     client.send_message(commands)
    client.close()

    # obstacle_data: list = client.receive()
    # client.close()
    # print("Got data from RPi:")
    # print(obstacle_data)

    # # obstacle_data = [
    # #     [105, 75, 180, 0],
    # #     [135, 25, 0, 1],
    # #     [195, 95, 180, 2],
    # #     [175, 185, -90, 3],
    # #     [75, 125, 90, 4],
    # #     [15, 195, -90, 5]
    # # ]
    # obstacles = parse_obstacle_data(obstacle_data)

    # if also_run_simulator:
    #     app = AlgoSimulator(obstacles)
    #     app.init()
    #     app.execute()

    # app = AlgoMinimal(obstacles)
    # app.init()
    # app.execute()

    # # Send the list of commands over.
    # print("Sending list of commands to RPi...")
    # commands = app.robot.convert_all_commands()
    # client.send_message(commands)
    # client.close()


def run_rpi():
    while True:
        run_minimal(False)
        time.sleep(5)


if __name__ == '__main__':
    run_minimal(False)
    # run_simulator()
