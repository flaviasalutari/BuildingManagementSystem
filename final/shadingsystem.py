# -*- coding: utf-8 -*-
import math
import random
import json
from configurationroom import configuration_room
from datetime import datetime

class ShadingSystem():

    def __init__(self):
        self.tint = configuration_room["Room"]["default_tint"]
        self.ex_intensity = 0
        self.threshold = configuration_room["Room"]["threshold_intensity"] # intensity threshold
        self.perc_tints = configuration_room["default"]["perc_tints"]      # transmittance of tints
        self.topic1 = "ShadowingSystem/GetIntensity"   # topic for ask values
        # self.topic2 = "ShadowingSystem/GetNpeople"  #    BY ACTIVATING THIS TOPIC THIS SYSTEM TAKES INTO ACCOUNT HUMAN PRESENCE IN THE ROOM, 
                                  


    def request_msg_intensity(self, client):
        msg1 = {
                "request": "get_intensity", 
                "timestamp": str(datetime.now()),
        }
        client.publish(self.topic1, json.dumps(msg1))
        self.read_1 = 0

        
    # def request_msg_people(self, client):            #    BY ACTIVATING THIS FUNCTION THIS SYSTEM TAKES INTO ACCOUNT HUMAN PRESENCE IN THE ROOM, 
                                                       #    IF NO ONE INSIDE IT JUST DOES NOTHING
    #     msg2 = {
    #             "request": "get_n_people", 
    #             "timestamp": str(datetime.now())
    #     }
    #     client.publish(self.topic2, json.dumps(msg2))
    #     self.read_2 = 0


    def read_msg(self, msg):
        try:
            obj_m = json.loads(str(msg))
            if obj_m["sensor_type"]== "intensity" and self.read_1 == 0:
                intensity = obj_m["intensity_sensed"]
                self.read_1 = 1
                print "\n intensity: " + str(intensity) 
                self.ex_intensity = intensity
                self.check_intensity()
            # elif obj_m["sensor_type"] == "people_counter" and self.read_2 == 0:    #    BY ACTIVATING THIS FUNCTION THIS SYSTEM TAKES INTO 
            #     self.read_2 = read_1                                               #    ACCOUNT HUMAN PRESENCE IN THE ROOM, 
            #     presence = obj_m["n_people_sensed"]                                #    IF NO ONE INSIDE IT JUST DOES NOTHING
            #     print "\n Number of people here : " + str(presence)
            else:
                pass
        except:
            print "Error in parsing the message _ intensty"

    def check_intensity(self):
        if self.ex_intensity>self.threshold: # intensity of solar radiation above threshold
            for tint in range(1,4):
                transmitted_intensity=self.perc_tints[tint]*self.ex_intensity
                if transmitted_intensity < self.threshold:
                    self.tint = tint # set earliest tint satisfying transmitted intensity below threshold
                    print "\n Transmitted intensity: " + str(transmitted_intensity)
                    print "\n The tint is: " + str(tint)
                    return
        else:  # set the lightest tint since external situation fine
            self.tint = 1
            print "\n The tint is : " + str(self.tint)
   


    