# -*- coding: utf-8 -*-
import random
import json
from datetime import datetime
from configurationroom import configuration_room

          
class PeopleCounter(): # It stands over the desk, in the dedicated column 
    
    def __init__(self, name):
        self.name = name
        self.topic = str(self.name) + "/NPeople" # topic on which the sensor publish the value sensed


    def parse_msg(self, msg, client, n_people):# parse the message to verify the request it is really addressed to him
        try:
            obj_m = json.loads(str(msg)) 
            print obj_m

            if obj_m["request"]== "get_n_people":
                self.sense_person(n_people, client) # call the sensing function
            else:
                pass
        except:
            print "Error in parsing the message _ SensorFlux"

        
    def sense_person(self, n_people, client):  # get number of people from environment 
        msg = {
                "sensor_type": "people_counter",
                "name": self.name, 
                "n_people_sensed": n_people, 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic, json.dumps(msg)) # publish message containing the sensed value