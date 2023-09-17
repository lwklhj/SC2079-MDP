import sys
import time
import pickle
from typing import List

import settings
from app import AlgoSimulator, AlgoMinimal
from entities.assets.direction import Direction
from entities.connection.rpi_client import RPiClient
from entities.connection.rpi_server import RPiServer
from entities.grid.obstacle import Obstacle


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
    obstacles = [
        [105, 75, 180, 0],
        [135, 25, 0, 1],
        [195, 95, 180, 2],
        [175, 185, -90, 3],
        [75, 125, 90, 4],
        [15, 195, -90, 5]
    ]
    obs = parse_obstacle_data(obstacles)
    app = AlgoSimulator(obs)
    app.init()
    app.execute()


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

    #data = []
    
    while True:
        data = client.socket.recv(4096)  # 1024 is the buffer size
        data = data.decode() # convert to string
        
        print("Got data from RPi:")
        print(data)

        data = data.split(',') # Split on delimiter

        obstacle_data = [] # Array for storing obstacle data
        
        i = 0
        while(i < len(data)):
            # Android formatted the data as below
            # Ori,x,y,no,ori2,x2,y2,no2
            obstacle_data.append((int(data[i+1]), int(data[i+2]), int(data[i+3]), int(data[i])))
            i =+ 4 # Every four strings is an obstacle
        obstacles = parse_obstacle_data(obstacle_data)

        if also_run_simulator:
            app = AlgoSimulator(obstacles)
            app.init()
            app.execute()

        app = AlgoMinimal(obstacles)
        app.init()
        app.execute()

        # Send the list of commands over.
        print("Sending list of commands to RPi...")
        commands = app.robot.convert_all_commands()
        client.send_message(commands)
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
