#!/usr/bin/env python3


# For general information on DHT sensors in Python, see Adafruit's helpful tutorials
# https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup

import Adafruit_DHT
import datetime
import json
import time

# Port 80 is easy but requires the script to be run as root
# If you'd prefer not to run as root, choose another port such as 8080
HTTP_PORT = 80

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_0_PIN = 4
DHT_1_PIN = 18

# Occassionally the sensor will return null values, especially if polled repeatedly in less than 3 seconds.
# This code will retry up to the MAX_TRIES number of times.
MAX_TRIES = 10

from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        tries = 0
        humidity_0 = None
        temperature_0 = None
        while (humidity_0 is None and temperature_0 is None and tries < MAX_TRIES):
            humidity_0, temperature_0 = Adafruit_DHT.read(DHT_SENSOR, DHT_0_PIN)
            tries += 1

        tries = 0
        humidity_1 = None
        temperature_1 = None
        while (humidity_1 is None and temperature_1 is None and tries < MAX_TRIES):
            humidity_1, temperature_1 = Adafruit_DHT.read(DHT_SENSOR, DHT_1_PIN)
            tries += 1

        th_data = {
                'sensor_0': {
                    'temperature': temperature_0,
                    'humidity': humidity_0
                    },
                'sensor_1': {
                    'temperature': temperature_1,
                    'humidity': humidity_1
                    }

                }

        json_data = json.dumps(th_data)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(json_data, 'utf-8'))

httpd = HTTPServer(('', HTTP_PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()

