# -*- coding: utf-8 -*-
import random
import json
from datetime import datetime
from configurationroom import configuration_room

class SensorFlux():  # It stands over the desk, in the dedicated column, its value is read by the lighting system

    def __init__(self, name):
        self.name = name
        self.topic = str(self.name) + "/Flux" # topic on which the sensor publish the value sensed

    def parse_msg(self, msg, client, flux): # parse the message to verify the request it is really addressed to him
        try:
            obj_m = json.loads(str(msg)) 
            print obj_m
            if obj_m["request"]== "get_flux":
                perc_tint = obj_m["perc_tint"] # transmittance factor of the actual tint in use
                artificial_flux = obj_m["artificial_flux"] 
                self.sense_flux(perc_tint+0.4, artificial_flux, flux, client) # call the sensing function
            else:
                pass
        except:
            print "Error in parsing the message _ SensorFlux"
        
    def sense_flux(self, perc_tint, artificial_flux, flux, client):  # get the sensed flux value due to both solar irradiation and number of lamps ON
        self.external_flux = flux # contribute given by external flux (environment)
        transmitted_flux = perc_tint*self.external_flux # amount of external luminous flux transmitted through the window due to tint in use
        print "TRANSMITTED FLUX : " + str(transmitted_flux)
        print "ARTIFICIAL FLUX : " + str(artificial_flux)
        total_flux = transmitted_flux + artificial_flux # total amount of flux in the room
        msg = {
                "sensor_type": "flux",
                "name": self.name, 
                "total_flux_sensed": total_flux, 
                "timestamp": str(datetime.now())
        }
        print msg
        client.publish(self.topic, json.dumps(msg)) # publish message containing the sensed value

 