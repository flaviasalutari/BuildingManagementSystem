import math
import random
import json
from fileconfig import *
from controllers_config import *

class ShadowingSystem():

    def __init__(self, tint, threshold):
        self.tint = tint
        self.ex_intensity = ""
        self.threshold = threshold
        self.perc_tints = perc_tints

    def read_msg(self, msg):
        try:
            obj_m = json.loads(str(msg))
            if obj_m["sensor_type"]== "intensity":
                intensity = obj_m["intensity_sensed"]
                print "\n intensity: " + str(intensity)
                self.ex_intensity = intensity
                self.check_intensity()
            else:
                pass
        except:
            print "Error in parsing the message _ intensty"

        
    def check_intensity(self):
        if self.ex_intensity>self.threshold:
            for tint in range(1,4):
                transmitted_intensity=perc_tints[tint]*self.ex_intensity
                if transmitted_intensity < self.threshold:
                    self.tint = tint
                    print "Transmitted intensity: " + str(transmitted_intensity)
                    print "\n The tint is: " + str(tint)
                    return
        else:
            self.tint = 1
            print "\n The tint is : " + str(self.tint)
   
class ArtificialLight():
    
    def __init__(self, required_flux, lumen_lamp, total_lamps):
        self.required_flux = required_flux
        self.lumen_lamp = lumen_lamp
        self.total_lamps = total_lamps
        self.active_lamps = int(random.uniform(0,total_lamps))
        
    def read_msg(self, msg):
        try:
            obj_m = json.loads(str(msg))
            print obj_m
            if obj_m["sensor_type"]== "flux":
                total_flux = obj_m["total_flux_sensed"]
                print "\n total_flux : " + str(total_flux)
                self.total_flux = total_flux
            elif obj_m["sensor_type"]== "PIR":
                presence = obj_m["n_people_sensed"]
                self.presence = presence
                if self.presence is not 0:
                    if self.total_flux < self.required_flux :
                        diff = self.required_flux - self.total_flux
                        n_lamps_required = math.ceil(diff / self.lumen_lamp)
                        print "\n Number of lamps to be switched ON: " + str(n_lamps_required)
                        self.actuator(n_lamps_required) 
                else:
                    pass 
            else: 
                pass
        except:
            print "Error in parsing the message _ flux"



            
    def actuator(self, n_lamps):
        self.active_lamps = self.active_lamps + n_lamps
        # pubblica e forza l'accensione di n_lamps lampade
        print "switched on: " + str(n_lamps)
        


class ControlAirQuality():
    
    def __init__(self):
        self.min_ACH = voc_numerator/classA

    
    def read_msg(self, msg): # get n_person fom dedicated sensor 
        try:
            obj_m = json.loads(str(msg))
            if obj_m["sensor_type"]== "PIR":
                n_people = obj_m["n_people_sensed"]
                print "\n n_people: " + str(n_people)
                self.n_people = n_people
            else:
                pass
        except:
            print "Error in parsing the message _ NPeople"

        
    def evaluate_voc(self):
        av_occupation = self.n_people * f_occupation
        self.ACH = q_iaq * av_occupation / volume
        
        
        # ERAVAMO QUAAAA
        
    
      
    
        
        
        
        
    