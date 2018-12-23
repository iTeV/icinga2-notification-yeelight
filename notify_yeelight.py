#!/usr/bin/python3
__author__ = "iTeV <iTeV@fs0ciety.xyz>"

try:
    import socket
    import json
    import time
    import os
except ImportError as e:
    print(e)


class NotifyYeelight:

    def __init__(self, bulbIP, port=55443):
        try:
            self.sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((bulbIP, port))
        except Exception as e:
            print(e)

    def get_current_state(self):
        """ Method to get current state of bulb (on/off) and current color"""
        data = {
                "id": 1,
                "method": "get_prop",
                "params": ["power", "rgb", "bright"]
                }
        response = self.send(data, True)
        self.state = response['result'][0]
        self.color = response['result'][1]
        self.bright = response['result'][2]

    def toggle(self):
        """ Method to toggle the bulb on/off """
        data = {
                "id": 1,
                "method": "toggle",
                "params": []
                }
        self.send(data)

    def set_brightness(self, lvl):
        """ Method to change brightness level"""
        """ lvl argument MUST be a int! """
        data = {
                "id": 1,
                "method": "set_bright",
                "params": [lvl]
                }
        self.send(data)

    def set_color(self, color):
        """ Method to set the color on the bulb """
        """ color arg MUST be a hex value! (0xFFFFFF)"""
        if type(color) == int:
            data = {
                    "id": 1,
                    "method": "set_rgb",
                    "params": [color]
                    }
            self.send(data)

    def blink_light(self, color, amount=3):
        """ Method to bink the bulb """
        self.get_current_state()
        if self.state == "off":
            self.toggle()
        self.set_color(color)
        for round in range(0, amount):
            self.set_brightness(100)
            time.sleep(0.5)
            self.set_brightness(1)
            time.sleep(0.5)
        # Save old state
        previousState = self.state
        previousBright = int(self.bright)
        previousColor = int(self.color)
        if previousState != "off":
            self.set_brightness(previousBright)
            self.set_color(previousColor)
        else:
            self.toggle()

    def send(self, data, return_data=False):
        """ Method to send data to the bulb """
        data = json.dumps(data)
        data += "\r\n"
        self.sock.send(data.encode())
        if return_data:
            returnData = self.sock.recv(1024).decode()
            return json.loads(returnData)


yeelight = NotifyYeelight("127.0.0.1")
lst_good = ["OK", "UP"]
lst_bad = ["CRITICAL", "DOWN"]
lst_warn = ["WARNING"]
if os.environ.get("STATE") in lst_good:
    yeelight.blink_light(0x15ff00)
elif os.environ.get("STATE") in lst_bad:
    yeelight.blink_light(0xff1000)
elif os.environ.get("STATE") in lst_warn:
    yeelight.blink_light(0xffff00)
