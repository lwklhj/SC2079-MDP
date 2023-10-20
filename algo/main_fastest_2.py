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
    # Change this
    obstacle_lt = 70
    ideal_distance = int(obstacle_lt/2 - 30)
    if (ideal_distance<=0):
        ideal_distance = 1
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
                    # Index which was used to recognise the image index in Week 8
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

                    # image_dict = {
                    #     11: "1",
                    #     12: "2",
                    #     13: "3",
                    #     14: "4",
                    #     15: "5",
                    #     16: "6",
                    #     17: "7",
                    #     18: "8",
                    #     19: "9",
                    #     20: "A",
                    #     21: "B",
                    #     22: "C",
                    #     23: "D",
                    #     24: "E",
                    #     25: "F",
                    #     26: "G",
                    #     27: "H",
                    #     28: "S",
                    #     29: "T",
                    #     30: "U",
                    #     31: "V",
                    #     32: "W",
                    #     33: "X",
                    #     34: "Y",
                    #     35: "Z",
                    #     36: 36,
                    #     37: 37,
                    #     38: 38,
                    #     39: 39,
                    #     40: 40
                    # }

                    for file in os.listdir(results[0].save_dir+'/labels'):
                        if file.endswith('.txt'):
                            with open(results[0].save_dir+'/labels/'+file, 'r') as f:
                                lines = f.readlines()
                                if lines:
                                    if len(lines) != 1:
                                        first_line = 0
                                        first_integer = int(
                                            lines[first_line].split()[0])
                                        while (first_integer == 2):
                                            first_line += 1
                                            first_integer = int(
                                                lines[first_line].split()[0])
                                            break
                                    else:
                                        first_integer = int(
                                            lines[0].split()[0])
                                        print(first_integer)
                                        print("Detected image:",
                                              classes[first_integer])

                    print(index)

                    # Navigating the first obstacle
                    if index == '1':
                        # Go right
                        print(index)
                        print((classes[first_integer]))
                        print(type(classes[first_integer]))
                        if classes[first_integer] == 'id38':
                            image_dict["first_image"] = 'R'
                            movement_list = ["r0090", "l0090","l0090", "r0090", "b0020"]
                            movement_list_1.extend(movement_list)

                            client.send_message(movement_list)
                        # Go left
                        elif classes[first_integer] == 'id39':
                            image_dict["first_image"] = 'L'
                            movement_list = ["l0090", "r0090","r0090", "l0090", "b0020"]
                            movement_list_1.extend(movement_list)
                            client.send_message(movement_list)

                    # Navigating second obstacle
                    if index == '2':
                        # Go right
                        return_y_list = []
                        final_movement_list = []
                        if classes[first_integer] == 'id38':
                            image_dict["second_image"] = 'R'
                            
                            movement_list = ["r0090", "f" + str(ideal_distance).rjust(4, "0"), "l0090", "f0010", "l0090", "f" + str(ideal_distance).rjust(
                            4, "0"), "f0050", "f" + str(ideal_distance).rjust(4, "0"), "l0090", "f0010"]
                            
                            return_y_list.extend(["l0090", "f" + str(ideal_distance).rjust(4, "0"), "r0090"])

                            if distance2:
                                # For moving directly to the centre
                                final_movement_list.extend(movement_list)
                                final_movement_list.extend(["f0050"])
                                final_movement_list.append("f" + str(distance2).rjust(4, "0"))
                                final_movement_list.extend(["f0045"])
                                final_movement_list.extend(return_y_list)
                                final_movement_list.append("f" + str(distance1).rjust(4, "0"))

                            else:
                                # For moving directly to the centre
                                final_movement_list.extend(movement_list)
                                final_movement_list.extend(["f0050"])
                                final_movement_list.extend(["f0045"])
                                final_movement_list.extend(return_y_list)
                                final_movement_list.append("f" + str(distance1).rjust(4, "0"))
                            client.send_message(final_movement_list)
                        
                        # Go left
                        elif classes[first_integer] == 'id39':
                            image_dict["second_image"] = 'L'
                            movement_list = ["l0090", "f" + str(ideal_distance).rjust(4, "0"),"r0090", "f0010", "r0090", "f" + str(ideal_distance).rjust(
                            4, "0"), "f0050", "f" + str(ideal_distance).rjust(4, "0"), "r0090", "f0010"]

                            return_y_list.extend(["r0090", "f" + str(ideal_distance).rjust(4, "0"), "l0090"])

                            if distance2:
                                # For moving directly to the centre
                                final_movement_list.extend(movement_list)
                                final_movement_list.extend(["f0050"])
                                final_movement_list.append("f" + str(distance2).rjust(4, "0"))
                                final_movement_list.extend(["f0045"])
                                final_movement_list.extend(return_y_list)
                                final_movement_list.append("f" + str(distance1).rjust(4, "0"))

                            else:
                                # For moving directly to the centre
                                final_movement_list.extend(movement_list)
                                final_movement_list.extend(["f0050"])
                                final_movement_list.extend(["f0045"])
                                final_movement_list.extend(return_y_list)
                                final_movement_list.append(
                                    "f" + str(distance1).rjust(4, "0"))
                            client.send_message(final_movement_list)
                        
                    count_scans += 1
                    if (2 == count_scans):
                        image_join.collate_images(folder_path)

                except Exception as e:
                    print("IMAGE RECOGNITION ERROR: ", e)
            # If the data is not an image, it is x distance travelled for first obstacle
            elif (data.split('|')[0] == "dist1"):
                print("RECEIVED DIST 1")
                distance1 = data.split('|')[1]  # Split on delimiter
                distance1 = str(int(distance1)-10)
            # If the data is not an image, it is x distance travelled for second obstacle
            elif (data.split('|')[0] == "dist2"):
                print("RECEIVED DIST 2")
                distance2 = data.split('|')[1]  # Split on delimiter

def reverse_commands(commands):
    reversed_commands = []
    reverse_dict = {
        'r': 'l',
        'l': 'r'
    }
    for command in commands:
        if command[0] != 'f' and command[0] != 'b':
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
