import math
import random
import json
from configuration_file import configuration_room
from datetime import datetime

class ShadowingSystem():

    def __init__(self):
        self.tint = configuration_room["Room"]["default_tint"]
        self.ex_intensity = ""
        self.threshold = configuration_room["Room"]["threshold"]
        self.perc_tints = configuration_room["default"]["perc_tints"]
        self.topic1 = "ShadowingSystem/GetIntensity"
        self.topic2 = "ShadowingSystem/GetNpeople"
        self.read_1 = ''
        self.read_2 = ''


    def request_msg_intensity(self, client):
        msg1 = {
                "request": "get_intensity", 
                "timestamp": str(datetime.now()),
        }
        client.publish(self.topic1, json.dumps(msg1))
        self.read_1 = 0

        
    def request_msg_people(self, client):
        msg2 = {
                "request": "get_n_people", 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic2, json.dumps(msg2))
        self.read_2 = 0


    def read_msg(self, msg):
        try:
            obj_m = json.loads(str(msg))
            if obj_m["sensor_type"]== "intensity" and self.read_1 == 0:
                intensity = obj_m["intensity_sensed"]
                self.read_1 = 1
                print "\n intensity: " + str(intensity) 
                self.ex_intensity = intensity
                self.check_intensity()
            elif obj_m["sensor_type"] == "PIR" and self.read_2 == 0:
                self.read_2 = 1
                presence = obj_m["n_people_sensed"]
                print "\n Number of people here : " + str(presence)
            else:
                pass
        except:
            print "Error in parsing the message _ intensty"

    def check_intensity(self):
        if self.ex_intensity>self.threshold:
            for tint in range(1,4):
                transmitted_intensity=self.perc_tints[tint]*self.ex_intensity
                if transmitted_intensity < self.threshold:
                    self.tint = tint
                    print "\n Transmitted intensity: " + str(transmitted_intensity)
                    print "\n The tint is: " + str(tint)
                    return
        else:
            self.tint = 1
            print "\n The tint is : " + str(self.tint)
   
class ArtificialLight():
    
    def __init__(self):
        self.required_flux = configuration_room["Room"]["required_flux"]
        self.lumen_lamp = configuration_room["Room"]["lumen_lamp"]
        self.total_lamps = configuration_room["Room"]["total_lamps"]
        self.active_lamps = int(random.uniform(0,self.total_lamps))
        self.topic1 = "ArtificialLight/GetFlux"
        self.topic2 = "ArtificialLight/GetNpeople"
        self.read1 = ''
        self.read2 = ''
        
    def request_msg_flux(self, client, perctint):
        msg1 = {
                "request": "get_flux", 
                "timestamp": str(datetime.now()),
                "active_lamps" : self.active_lamps,
                "perc_tint" : perctint
        }
        
        client.publish(self.topic1, json.dumps(msg1))
        self.read1 = 0


    def request_msg_people(self, client):
        msg2 = {
                "request": "get_n_people", 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic2, json.dumps(msg2))
        self.read2 = 0

    def read_msg(self, msg):
       # try:
        obj_m = json.loads(str(msg))
        if obj_m["sensor_type"]== "flux" and self.read1 == 0:
            self.read1 = 1
            total_flux = obj_m["total_flux_sensed"]
            print "\n total_flux : " + str(total_flux)
            self.total_flux = total_flux
        elif obj_m["sensor_type"] == "PIR" and self.read2 == 0:
            self.read2 = 1
            presence = obj_m["n_people_sensed"]
            self.presence = presence
            if self.presence is not 0:
                if self.total_flux < self.required_flux :
                    diff = self.required_flux - self.total_flux
                    n_lamps_required = math.ceil(diff / self.lumen_lamp)
                    print "\n Number of lamps to be switched ON: " + str(n_lamps_required)
                    self.actuator(n_lamps_required) 
                else:
                    print "\n No additional lamps to be switched OFF"
                    
            else:
                pass 
        else: 
                pass

                
       # except:
       #     print "Error in parsing the message _ flux"



            
    def actuator(self, n_lamps):
        self.active_lamps = self.active_lamps + n_lamps
        print "switched on: " + str(n_lamps) 
        


class ControlAirQuality():
    
    def __init__(self):
        self.voc_numerator = self.evaluate_num()
        self.min_ACH = self.voc_numerator/configuration_room["default"]["classA"]
        self.topic = "ControlAirQuality/GetNpeople"

    def evaluate_num(self):
        voc_numerator = 0
        f_emissions = configuration_room["Room"]["TVOC"]["f_emission"]
        surfaces = configuration_room["Room"]["TVOC"]["surface"]
        for key in f_emissions.keys():
            voc_numerator += f_emissions[key] * surfaces[key]
        voc_numerator = voc_numerator/(configuration_room["Room"]["volume"]* 0.9)
        return voc_numerator

    def request_msg_people(self, client):
        msg = {
                "request": "get_n_people", 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic, json.dumps(msg))

    def read_msg(self, msg): # get n_person fom dedicated sensor 
        try:
            obj_m = json.loads(str(msg))
            if obj_m["sensor_type"]== "PIR":
                n_people = obj_m["n_people_sensed"]
                print "\n n_people: " + str(n_people)
                self.n_people = n_people
                self.evaluate_voc()
            else:
                pass
        except:
            print "Error in parsing the message _ NPeople"

        
    def evaluate_voc(self):
        av_occupation = self.n_people * configuration_room["Room"]["f_occupation"]
        self.ACH = configuration_room["Room"]["q_iaq"] * av_occupation/ configuration_room["Room"]["volume"]
        if self.ACH < self.min_ACH:
            diff = self.min_ACH - self.ACH
            print "\n ACH not satisfied. Increase ACH of: " + str(diff)

        else:
            print "\n Min ACH satisfied"

        
            
    
      
    
        
        
        
        
    