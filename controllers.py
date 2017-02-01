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
            elif obj_m["sensor_type"] == "people_counter" and self.read_2 == 0:
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
   
class LightController():
    
    def __init__(self):
        self.required_flux = configuration_room["Room"]["required_flux"]
        self.lumen_lamp_desk = configuration_room["Room"]["lumen_lamp_desk"]
        self.lumen_lamp_ambient = configuration_room["Room"]["lumen_lamp_ambient"]
        self.total_lamps_desk = configuration_room["Room"]["total_lamps_desk"]
        self.lamps_per_ambient= configuration_room["Room"]["lamps_per_ambient"]
        self.total_ambients= configuration_room["Room"]["total_ambients"]
        self.active_lamps_desk = 0
        self.active_ambients = 0
        self.topic1 = "LightController/GetFlux"
        self.topic2 = "LightController/GetNpeople"
        self.read1 = ''
        self.read2 = ''
        self.total_flux = 0
        
    def request_msg_flux(self, client, perctint):
        msg1 = {
                "request": "get_flux", 
                "timestamp": str(datetime.now()),
                "artificial_flux" : self.artificial_flux(),
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
        elif obj_m["sensor_type"] == "people_counter" and self.read2 == 0:
            self.read2 = 1
            presence = obj_m["n_people_sensed"]
            self.presence = presence
            if self.presence is not 0:
                if self.total_flux < self.required_flux :
                    diff = self.required_flux - self.total_flux
                    # if diff > 0:
                    if self.active_lamps_desk==0:
                        self.active_lamps_desk = 1
                        print "Lamps on desk are now ON"
                        diff = diff - (self.total_lamps_desk * self.lumen_lamp_desk)
                        while diff > 0:
                            self.active_ambients += 1    
                            diff = diff - (self.lumen_lamp_ambient* self.lamps_per_ambient)
                        print "Lamps switched ON over: " + str(self.active_ambients) + " ambients"
                    else:
                        to_activate = 0
                        while diff > 0:
                            to_activate += 1    
                            diff = diff - (self.lumen_lamp_ambient * self.lamps_per_ambient)
                        self.active_ambients += to_activate
                        print "Lamps on desk already ON, Lamps switched ON over: " + str(to_activate) + " ambients"
                    self.actuator() 
                else:
                    diff = self.total_flux - self.required_flux
                    if self.active_ambients > 0:
                        tot_lumen_ambient = (self.lumen_lamp_ambient * self.lamps_per_ambient)
                        n_ambient_to_be_switched_off = int(diff/tot_lumen_ambient)
                        if n_ambient_to_be_switched_off > self.total_ambients:
                            self.total_ambients = 0
                            print "Switched OFF all the ambients"
                        else:
                            self.total_ambients -= n_ambient_to_be_switched_off
                            print "\nSwitched OFF : " + str(n_ambient_to_be_switched_off) + " ambients"
                    if self.active_lamps_desk==1:
                        if self.total_lamps_desk * self.lumen_lamp_desk < diff:
                            self.active_lamps_desk = 0
                            print "\nLamps on desk are switched OFF"
                        else:
                            print "\nLamps on desks are not switched OFF"

                if self.active_lamps_desk == 1:
                    print "- - - - - - - - -"
                    print "LAMPS ON DESKS ARE ON + " + str(self.active_ambients) + " AMBIENTS ACTIVE"   
                    print "- - - - - - - - -"
                else:
                    print "- - - - - - - - -"
                    print "ALL THE LAMPS ARE OFF"   
                    print "- - - - - - - - -"                            
            else:
                print "\n No people in the room so nothing to be switched ON"
                self.active_lamps_desk = 0
                self.active_ambients = 0
        else: 
            pass

                
       # except:
       #     print "Error in parsing the message _ flux"

    def artificial_flux(self):
        artificial_flux = (self.active_lamps_desk * self.total_lamps_desk * self.lumen_lamp_desk) +\
                            (self.active_ambients * self.lamps_per_ambient * self.lumen_lamp_ambient)
        return artificial_flux

            
    def actuator(self):
        print "Switch ON" 
        


class ControlAirQuality():
    
    def __init__(self):
        self.voc_numerator = self.evaluate_num()
        self.min_ACH = self.voc_numerator/configuration_room["default"]["classA"]
        self.topic = "ControlAirQuality/GetNpeople"
        self.q_iaq = float(configuration_room["Room"]["q_iaq"])
        self.f_occupation = configuration_room["Room"]["f_occupation"]
        self.ACH = 0

    def evaluate_num(self):
        voc_numerator = 0
        f_emissions = configuration_room["Room"]["TVOC"]["f_emission"]
        surfaces = configuration_room["Room"]["TVOC"]["surface"]
        for key in f_emissions.keys():
            voc_numerator += f_emissions[key] * surfaces[key]
        voc_numerator = float(voc_numerator)/float(configuration_room["Room"]["volume"] * configuration_room["default"]["occupancy_coefficient"])
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
            if obj_m["sensor_type"]== "people_counter":
                n_people = obj_m["n_people_sensed"]
                print "\n n_people: " + str(n_people)
                self.n_people = n_people
                self.evaluate_voc()
            else:
                pass
        except:
            print "Error in parsing the message _ NPeople"

    def evaluate_ach(self):

        if self.n_people == 0:
            self.ACH=0
            self.q_iaq=0
        else:
            av_occupation = float(self.n_people)
            volume = float(configuration_room["Room"]["volume"])
            self.ACH = self.q_iaq * av_occupation/ volume
            if self.ACH < self.min_ACH:
                diff = self.min_ACH - self.ACH
                print "\n ACH not satisfied. Increase ACH of: " + str(diff)
                self.q_iaq = (self.ACH+diff) * volume / av_occupation
                self.ACH = self.q_iaq * av_occupation/ volume

            else:
                diff = self.ACH - self.min_ACH
                print "\n Min ACH satisfied. Decrease ACH of: " + str(diff)
                self.q_iaq = (self.ACH-diff) * volume / av_occupation
                self.ACH = self.q_iaq * av_occupation/ volume
        # ERAVAMO QUAAA


    