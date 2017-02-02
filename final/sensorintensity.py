# -*- coding: utf-8 -*-
import random
import json
from datetime import datetime
from configurationroom import configuration_room


class SensorIntensity(): # It stands outside the window, its value is read by the shadowing system
    
    def __init__(self, name):
        self.name = name 
        self.topic = str(self.name) + "/Intensity" # topic on which the sensor publish the value sensed

    def parse_msg(self, msg, client, intensity): # parse the message to verify the request it is really addressed to him
        try:
            obj_m = json.loads(str(msg))
            print obj_m
            if obj_m["request"]== "get_intensity":
                self.sense_intensity(intensity, client) # call the sensing function
            else:
                pass
        except:
            print "Error in parsing the message _ SensorIntensity"

    def sense_intensity(self, intensity, client): # get intensity value from environment 
        intensity = (intensity + random.uniform(0,1)*0.05)/1.05 # emulates some random noise 
        msg = {
                "sensor_type": "intensity",
                "name": self.name,
                "intensity_sensed": intensity, 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic, json.dumps(msg)) # publish message containing the sensed value




