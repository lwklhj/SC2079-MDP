import sys
import time
import pickle
from typing import List

import image_join as image_join
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

    buffer = []
    count_scans = 0
    # Commands for first obstacle
    movement_list_1 = []
    # Commands for second obstacle
    movement_list_2 = []
    # Image dictionary
    image_dict = {
        "first_image": '',
        "second_image": ''
    }
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
                    #Index which was used to recognise the image index in Week 8
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
                    MODEL_FILE_PATH = '/Users/jordan/Documents/Github/SC2079-MDP/algo/kenze.pt'
                    model = YOLO(MODEL_FILE_PATH)
                    folder_path = "/Users/jordan/Documents/Github/SC2079-MDP/algo/predictions"
                    # Start imrec
                    results = model.predict(img, save=True, imgsz=640, conf=0.5, save_txt=True,
                                            save_conf=True, project=folder_path)
                    classes = results[0].names

                    image_dict = {
                        11: "1",
                        12: "2",
                        13: "3",
                        14: "4",
                        15: "5",
                        16: "6",
                        17: "7",
                        18: "8",
                        19: "9",
                        20: "A",
                        21: "B",
                        22: "C",
                        23: "D",
                        24: "E",
                        25: "F",
                        26: "G",
                        27: "H",
                        28: "S",
                        29: "T",
                        30: "U",
                        31: "V",
                        32: "W",
                        33: "X",
                        34: "Y",
                        35: "Z",
                        36: 36,
                        37: 37,
                        38: 38,
                        39: 39,
                        40: 40
                    }

                    for file in os.listdir(results[0].save_dir+'/labels'):
                        if file.endswith('.txt'):
                            with open(results[0].save_dir+'/labels/'+file, 'r') as f:
                                lines = f.readlines()
                                if lines:
                                    first_integer = int(lines[0].split()[0])
                                    print(first_integer)
                                    print("Detected image:",
                                          classes[first_integer])

                    # Navigating the first obstacle
                    if index == 1:
                        # Go right
                        if classes[first_integer] == 0:
                            image_dict["first_image"] = 'R'
                            movement_list = ["r0090", "l0090",
                                             "f0005", "l0090", "r0090","b0010"]
                            movement_list_1.extend(movement_list)
                            client.send_message(movement_list)
                        # Go left
                        elif classes[first_integer] == 1:
                            image_dict["first_image"] = 'L'
                            movement_list = ["l0090", "r0090",
                                             "f0010", "r0090", "l0090","b0010"]
                            movement_list_1.extend(movement_list)
                            client.send_message(movement_list)

                    # Navigating second obstacle
                    if index == 2:
                        # Go right
                        if classes[first_integer] == 0:
                            image_dict["second_image"] = 'R'
                            movement_list = ["r0090","l0020"]
                            client.send_message(movement_list)
                        # Go left
                        elif classes[first_integer] == 1:
                            image_dict["second_image"] = 'L'
                            movement_list = ["l0090","r0020"]
                            client.send_message(movement_list)

                    count_scans += 1
                    if (2 == count_scans):
                        image_join.collate_images(folder_path)

                except Exception as e:
                    print("IMAGE RECOGNITION ERROR: ", e)
            # If the data is not an image, it is x distance travelled for first obstacle
            elif (data.split('|')[0] == "dist1"):
                distance1 = data.split('|')[1]  # Split on delimiter
            # If the data is not an image, it is x distance travelled for second obstacle 
            elif (data.split('|')[0] == "dist2"):
                distance2 = data.split('|')[1]  # Split on delimiter
            # If the data is not an image, it is y distance travelled from IR 
            elif (data.split('|')[0] == "IR"):
                ideal_distance = data.split('|')[1]
                direction = image_dict["second_image"]
                final_movement_list = []
                reverse_movement_list_1 = reverse_commands(movement_list_1)
                match direction:
                    case 'L':
                        movement_list_2.extend(["r0090","f0010","r0090",f"f00{ideal_distance}","f0050",f"f00{ideal_distance}","r0090","f0010","r0090",f"f00{ideal_distance}","l0090"])
                    case 'R':
                        movement_list_2.extend(["l0090","f0010","l0090",f"f00{ideal_distance}","f0050",f"f00{ideal_distance}","l0090","f0010","l0090",f"f00{ideal_distance}","r0090"])
                if distance2:
                    final_movement_list.extend(movement_list_2)
                    final_movement_list.append(f"f00{distance2}")
                    final_movement_list.extend(reverse_movement_list_1)
                    final_movement_list.append(f"f00{distance1}")
                else:
                    final_movement_list.extend(movement_list_2)
                    final_movement_list.extend(reverse_movement_list_1)
                    final_movement_list.append(f"f00{distance1}")   
                    
                client.send_message(final_movement_list)
             

        # send command and add it in a stack as well, to use the stack for the return process.

    # while True:
    #     received = client.socket.recv(64768000)  # 4096 is the buffer size
    #     buffer.append(received)
    #     # Join bytes into byte string
    #     data = b''.join(buffer)
    #     data = data.decode()
    #     # No more incoming bytes
    #     # Start operations
    #     if "!" in data:
    #         # Reset buffer
    #         buffer.clear()
    #         data = data.replace("!", "")
    #         print(type(data))
    #         # print(data)
    #         if (data.split('|')[0] == "img"):
    #             try:

    #                 print("1st")
    #                 index = data.split('|')[1]
    #                 print("2nd")
    #                 image_data_base64 = data.split('|')[2]

    #                 print(len(image_data_base64))

    #                 image_data_base64 = image_data_base64[2:len(
    #                     image_data_base64)-1]

    #                 # buffer needed for multiple of 4
    #                 # buffer_needed = 4 -((len(image_data_base64)) %4)
    #                 # image_data_base64 += '=' * buffer_needed

    #                 print(image_data_base64[:50])
    #                 print(image_data_base64[-50:])
    #                 print(len(image_data_base64))
    #                 print(type(image_data_base64))

    #                 img = pickle.loads(base64.b64decode(image_data_base64))
    #                 print("3rd")
    #                 # Load Model
    #                 MODEL_FILE_PATH = '/Users/jordan/Documents/Github/SC2079-MDP/algo/best.pt'
    #                 model = YOLO(MODEL_FILE_PATH)
    #                 folder_path = "/Users/jordan/Documents/Github/SC2079-MDP/algo/predictions"
    #                 # Start imrec
    #                 results = model.predict(img, save=True, imgsz=640, conf=0.5, save_txt=True,
    #                                         save_conf=True, project=folder_path)
    #                 classes = results[0].names
    #                 for file in os.listdir(results[0].save_dir+'/labels'):
    #                     if file.endswith('.txt'):
    #                         with open(results[0].save_dir+'/labels/'+file, 'r') as f:
    #                             lines = f.readlines()
    #                             if lines:
    #                                 first_integer = int(lines[0].split()[0])
    #                                 print(first_integer)
    #                                 print("Detected image:",
    #                                       classes[first_integer])
    #                 # Send result back
    #                 response = f"imgID|{index}|{classes[first_integer]}"
    #                 # if (len(data.split("|") == 4)):
    #                 #     response += f"|{data.split('|')[3]}"

    #                 client.send_message(response)
    #                 count_scans += 1
    #                 if(len(obstacles)==count_scans):
    #                     image_join.collate_images(folder_path)
    #             except Exception as e:
    #                 print("IMAGE RECOGNITION ERROR: ", e)

    #         else:
    #             data = data.split(',')  # Split on delimiter

    #             obstacle_data = []  # Array for storing obstacle data

    #             i = 0
    #             while (i < len(data)):
    #                 # Android formatted the data as below
    #                 # Ori,x,y,no,ori2,x2,y2,no2
    #                 obstacle_data.append(
    #                     (int(data[i]), int(data[i+1]), int(data[i+2]), int(data[i+3])))
    #                 i += 4  # Every four strings is an obstacle
    #             obstacles = parse_obstacle_data(obstacle_data)

    #             if also_run_simulator:
    #                 app = AlgoSimulator(obstacles)
    #                 app.init()
    #                 threading.Thread(target=app.execute).start()

    #             app = AlgoMinimal(obstacles)
    #             app.init()
    #             app.execute()

    #             # Send the list of commands over.
    #             print("Sending list of commands to RPi...")
    #             commands = app.robot.convert_all_commands()
    #             client.send_message(commands)

def reverse_commands(commands):
    reversed_commands = []
    reverse_dict = {
        'r': 'l',
        'l': 'r'
    }
    for command in commands:
        if command[0] != 'f' or command[0] != 'b':
            command = reverse_dict[command[0]] + command[1:]
        reversed_commands.append(command)
    return reversed_commands

def run_rpi():
    while True:
        run_minimal(False)
        time.sleep(5)


if __name__ == '__main__':
    run_minimal(False)
    # run_simulator()
