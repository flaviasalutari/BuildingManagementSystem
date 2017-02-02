# -*- coding: utf-8 -*-
import math
import random
import json
from configurationroom import configuration_room
from datetime import datetime


class ControlAirQuality():
    
    def __init__(self):
        self.voc_numerator = self.evaluate_num() # evaluate numerator of the voc formula
        self.topic = "ControlAirQuality/GetNpeople" # topic for ask values
        self.f_occupation = configuration_room["Room"]["f_occupation"]  # factor of occupation from configfile
        self.min_ACH = self.voc_numerator/configuration_room["default"]["classA"] # evaluate minimum ach to satisfy
        self.q_iaq = self.evaluate_q_iaq() #evaluate qiaq satisfying requirements
        self.n_people = 0
        self.ACH = 0

    def evaluate_num(self):
        voc_numerator = 0
        f_emissions = configuration_room["Room"]["TVOC"]["f_emission"]
        surfaces = configuration_room["Room"]["TVOC"]["surface"]
        for key in f_emissions.keys():
            voc_numerator += f_emissions[key] * surfaces[key]
        voc_numerator = float(voc_numerator)/float(configuration_room["Room"]["volume"] * configuration_room["default"]["occupancy_coefficient"])
        return voc_numerator

    def evaluate_q_iaq(self):
        q_iaq = self.min_ACH * configuration_room["Room"]["volume"]/ float(configuration_room["Room"]["avg_npeople"] * self.f_occupation)
        return q_iaq

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
                self.evaluate_ach()   # evaluate the ach value
            else:
                pass
        except:
            print "Error in parsing the message _ NPeople"

    def evaluate_ach(self):

        if self.n_people == 0:
            self.ACH=0 # nothing done in the case of no people in the room
        else:
            av_occupation = float(self.n_people) * self.f_occupation # dynamically evaluate average occupation due to presence of people in the room
            volume = float(configuration_room["Room"]["volume"])
            self.required_ACH = self.q_iaq * av_occupation/ volume # ach needed to satisfy the  requirement with actual number of people 
            if self.required_ACH < self.min_ACH: # required ach lower than minimum 
                self.ACH = self.min_ACH # set the minimum
                print "\nRequired ACH lower than the minimum one, ACH set to the minimum one : " + str(self.ACH)
            else:
                self.ACH = self.required_ACH # set the required one
                print "\nRequired ACH greater than minimum ACH, ACH set to the required one: " + str(self.ACH)

        # ERAVAMO QUAAA
