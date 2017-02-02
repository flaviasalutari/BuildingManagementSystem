# -*- coding: utf-8 -*-
import math
import random
import json
from configurationroom import configuration_room 
from datetime import datetime


""" 	                    
the policy to switch ON the lights is:
1 - the ones over the desks
2 - if requirements still not satisfied:
	2.1 - switch ON the ones farthest from the windows
	2.2 - switch ON the ones in the MIDDLE
	2.3 - switch ON the closest to the window
"""

class LightController():
    
    def __init__(self):
        self.required_flux = configuration_room["Room"]["required_flux"]      # flux due to requirements
        self.lumen_lamp_desk = configuration_room["Room"]["lumen_lamp_desk"]  # luminous flux of each lamp over the desks
        self.lumen_lamp_ambient = configuration_room["Room"]["lumen_lamp_ambient"] # luminous flux of each lamp in the other 3 ambients
        self.total_lamps_desk = configuration_room["Room"]["total_lamps_desk"] # number of lamps over the desks
        self.lamps_per_ambient= configuration_room["Room"]["lamps_per_ambient"] # number of lamps in each ambient
        self.total_ambients= configuration_room["Room"]["total_ambients"] # number of total ambients 
        self.active_lamps_desk = 0 # number of active lamps over the desks
        self.active_ambients = 0 # number of active lamps over the other ambients
        self.topic1 = "LightController/GetFlux" # initialize the topics for the desired information
        self.topic2 = "LightController/GetNpeople"
        self.read1 = '' # readX flag to identify if the msg from the topicX has been already read
        self.read2 = ''
        self.total_flux = 0
        
    def request_msg_flux(self, client, perctint):
        msg1 = {
                "request": "get_flux", 
                "timestamp": str(datetime.now()),
                "artificial_flux" : self.artificial_flux(),
                "perc_tint" : perctint
        }
        
        client.publish(self.topic1, json.dumps(msg1)) # request value from sensor
        self.read1 = 0


    def request_msg_people(self, client):
        msg2 = {
                "request": "get_n_people", 
                "timestamp": str(datetime.now())
        }
        client.publish(self.topic2, json.dumps(msg2))
        self.read2 = 0

    def read_msg(self, msg):
       try:
	        obj_m = json.loads(str(msg))
	        if obj_m["sensor_type"]== "flux" and self.read1 == 0: # if msg not read yet, read it
	            self.read1 = 1 # message read 
	            total_flux = obj_m["total_flux_sensed"] 
	            print "\ntotal_flux : " + str(total_flux)
	            self.total_flux = total_flux
	        elif obj_m["sensor_type"] == "people_counter" and self.read2 == 0:
	            self.read2 = 1
	            presence = obj_m["n_people_sensed"] # n of people in room
	            self.presence = presence 
	            self.actuator() 
	        else: 
	            pass

                
       except:
           print "Error in parsing the message _ flux"

    def artificial_flux(self):
        artificial_flux = (self.active_lamps_desk * self.total_lamps_desk * self.lumen_lamp_desk) +\
                            (self.active_ambients * self.lamps_per_ambient * self.lumen_lamp_ambient) # totalflux given by sum of natural and 
                           																			  # artificial contributes
        return artificial_flux

            
    def actuator(self):
        if self.presence is not 0:  # if someone is inside 
            if self.total_flux < self.required_flux : # lower than requirements 
                diff = self.required_flux - self.total_flux # evaluate how much has to be compensated
                if self.active_lamps_desk==0: # if all the lamps are OFF, i.e. lamps ON the desk are OFF
                    self.active_lamps_desk = 1 # activate them
                    print "Lamps on desk are now ON"
                    diff = diff - (self.total_lamps_desk * self.lumen_lamp_desk) # check the requirement fulfillment
                    while diff > 0:
                        self.active_ambients += 1    # switch ON on other ambients following the policy LEFT-RIGHT
                        diff = diff - (self.lumen_lamp_ambient* self.lamps_per_ambient)
                    print "Lamps switched ON over: " + str(self.active_ambients) + " ambients"
                else: # lamp on desk already active 
                    to_activate = 0 
                    while diff > 0: # check the requirement fulfillment
                        to_activate += 1    # n ambients to SWITCH ON
                        diff = diff - (self.lumen_lamp_ambient * self.lamps_per_ambient) 
                    self.active_ambients += to_activate  # switch the required ambients
                    print "Lamps on desk already ON, Lamps switched ON over: " + str(to_activate) + " ambients"
            else: # requirement fulfilled
                diff = self.total_flux - self.required_flux # how much can be saved
                if self.active_ambients > 0: # if at least one ambient is ON 
                    tot_lumen_ambient = (self.lumen_lamp_ambient * self.lamps_per_ambient) # total luminous flux per ambient
                    n_ambient_to_be_switched_off = int(diff/tot_lumen_ambient) # how many ambients to switch off 
                    if n_ambient_to_be_switched_off > self.total_ambients: # if the ambients to switch off are more than the actual ones
                        self.total_ambients = 0			# switch oFF all the ambients
                        print "Switched OFF all the ambients"
                    else:
                        self.total_ambients -= n_ambient_to_be_switched_off  # switch OFF only the needed ones
                        print "\nSwitched OFF : " + str(n_ambient_to_be_switched_off) + " ambients"
                if self.active_lamps_desk==1:   # lamps on desk still active
                    if self.total_lamps_desk * self.lumen_lamp_desk < diff: # if by switching off the lamps requirement is still satisfied
                        self.active_lamps_desk = 0 # switch them off 
                        print "\nLamps on desk are switched OFF"
                    else:
                        print "\nLamps on desks are not switched OFF"

            if self.active_lamps_desk == 1: # print only for visualization purpose
                print "- - - - - - - - -"
                print "LAMPS ON DESKS ARE ON + " + str(self.active_ambients) + " AMBIENTS ACTIVE"   
                print "- - - - - - - - -"
            else:
                print "- - - - - - - - -"
                print "ALL THE LAMPS ARE OFF"   
                print "- - - - - - - - -"                            
        else: 
            print "\n No people in the room so nothing to be switched ON"
            self.active_lamps_desk = 0 # switch off everything
            self.active_ambients = 0