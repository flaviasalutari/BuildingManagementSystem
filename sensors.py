import random
import json
from datetime import datetime



class SensorIntensity(): # Si trova all'esterno, il suo valore e letto dallo shadowing system
    
    def __init__(self, name):
        self.name = name
        self.topic = str(self.name) + "/Intensity"

    def parse_msg(self, msg, client, intensity): # get n_person fom dedicated sensor 
#        try:
        obj_m = json.loads(str(msg))
        print obj_m
        if obj_m["request"]== "get_intensity":
            self.sense_intensity(intensity, client)
        else:
            pass
#        except:
#            print "Error in parsing the message _ SensorIntensity"

    def sense_intensity(self, intensity, client):
        intensity = intensity + random.uniform(0,1)*0.05 # random rumore
        msg = {
                "sensor_type": "intensity",
                "name": self.name,
                "intensity_sensed": intensity, 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic, json.dumps(msg))

class SensorFlux(): # Si trova sopra la scrivania , nella colonna dei sensori. e letto dall artificial light

    def __init__(self, name):
        self.name = name
        self.topic = str(self.name) + "/Flux"


    def parse_msg(self, msg, client, flux, shadowing_system, artificial_light): # get n_person fom dedicated sensor 
#        try:
        obj_m = json.loads(str(msg))
        if obj_m["request"]== "get_flux":
            self.sense_flux(shadowing_system, artificial_light, flux, client)
        else:
            pass
#        except:
#            print "Error in parsing the message _ SensorFlux"
        
    def sense_flux(self, shadowing_system, artificial_light, flux,client):
        self.lumen_lamp=artificial_light.lumen_lamp
        self.active_lamps= artificial_light.active_lamps
        self.external_flux = flux

        artificial_flux = self.active_lamps * self.lumen_lamp
        tint=shadowing_system.tint
        transmitted_flux = shadowing_system.perc_tints[tint]*self.external_flux
        total_flux = transmitted_flux + artificial_flux
        msg = {
                "sensor_type": "flux",
                "name": self.name, 
                "total_flux_sensed": total_flux, 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic, json.dumps(msg))

           
class SensorPersonCounter():
    
    def __init__(self, name):
        self.name = name
        self.topic = str(self.name) + "/NPeople"


    def parse_msg(self, msg, client, n_people): # get n_person fom dedicated sensor 
#        try:
        obj_m = json.loads(str(msg))
        if obj_m["request"]== "get_n_people":
            self.sense_person(n_people, client)
        else:
            pass
#        except:
#            print "Error in parsing the message _ SensorFlux"

        
    def sense_person(self, n_people, client):
        msg = {
                "sensor_type": "PIR",
                "name": self.name, 
                "n_people_sensed": n_people, 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic, json.dumps(msg))


