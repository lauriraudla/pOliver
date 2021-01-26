from threading import Thread
import cv2
import asyncio
import websockets
import json
import config


class Referee:
    """
    Class that continuously reads commands from referee server websocket
    """

    def __init__(self, ws):
        self.go = None
        self.stopped = False
        self.robot = "pOliver"
        self.ws = ws


    def start(self):
        Thread(target=self.listen, args=()).start()
        return self

    def listen(self):

        while not self.stopped:
            message = self.ws.recv()
            command = json.loads(message)

            if command["signal"] == "stop" and self.robot in command["targets"]:
                self.go = False
            elif command["signal"] == "start" and self.robot in command["targets"]:
                index = command["targets"].index(self.robot)
                color = command["baskets"][index]
                config.set("vision", "basket_color", color)
                config.save()
                print(color)
                self.go = True
            else:
                pass





    def stop(self):
        self.stopped = True
