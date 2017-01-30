import random
import json
from datetime import datetime
from configuration_file import configuration_room


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


    def parse_msg(self, msg, client, flux): # get n_person fom dedicated sensor 
#        try:
        obj_m = json.loads(str(msg))
        print obj_m
        if obj_m["request"]== "get_flux":
            perc_tint = obj_m["perc_tint"]
            active_lamps = obj_m["active_lamps"]
            self.sense_flux(perc_tint, active_lamps, flux, client)
        else:
            pass
#        except:
#            print "Error in parsing the message _ SensorFlux"
        
    def sense_flux(self, perc_tint, active_lamps, flux, client):
        lumen_lamp= configuration_room["Room"]["lumen_lamp"]
        self.external_flux = flux
        artificial_flux = active_lamps * lumen_lamp
        transmitted_flux = perc_tint*self.external_flux
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
        print obj_m

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


