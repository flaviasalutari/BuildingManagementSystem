# -*- coding: utf-8 -*-
import time
import sys        
from environment import Environment
import paho.mqtt.client as mqtt   
from configurationbroker import configuration_broker    
from sensorintensity import SensorIntensity
from sensorflux import SensorFlux
from peoplecounter import PeopleCounter


outside_environment = Environment() # initialize environment, external parameters generator
outside_environment.run_environment() # generate environmental parameters

sensor_intensity = SensorIntensity("sensor_intensity") #initialize intensity sensor
sensor_flusso = SensorFlux("sensor_flusso") #initialize flux sensor
sensor_people = PeopleCounter("sensor_people") #initialize people counter sensor


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) # Show the connection result
    client.subscribe("#")       

def Intensity_callback(client, userdata, msg):
    sensor_intensity.parse_msg(msg.payload, client, outside_environment.intensity) # intensity sensor parse messages coming from "/GetIntensity" topic

def Flux_callback(client, userdata, msg):
    sensor_flusso.parse_msg(msg.payload, client, outside_environment.flux) # flux sensor parse messages coming from "/GetFlux" topic
    
def Nperson_callback(client, userdata, msg):
    sensor_people.parse_msg(msg.payload, client, outside_environment.n_people) # people counter parse messages coming from "/GetNpeople" topic

def main():
    

    try:
        client = mqtt.Client("Sensors")       # Create the client mqtt instance to send and retrieve messages to and from the broker 
        client.connect(configuration_broker["IPbroker"], configuration_broker["port"], 60) 	 # Connection of the mqtt client instance to the broker
        client.on_connect = on_connect  # Call the function to show the connection result
        client.message_callback_add("+/GetIntensity", Intensity_callback) # This topic is used to retrieve messages coming from "/GetIntensity" topic
        client.message_callback_add("+/GetFlux", Flux_callback) # This topic is used to retrieve retrieve messages coming from "/GetFlux" topic
        client.message_callback_add("+/GetNpeople", Nperson_callback) # This topic is used to retrieve retrieve messages coming from "/GetNpeople" topic
        client.loop_start()  # Enter in the loop state the mqtt client connection
    except:
        sys.exit("Connection to the broker failed")  # raise error in case of failed connection to the broker
       
    
    while(1): 
        outside_environment.run_environment() # generate environmental parameters
   
    
if __name__ == "__main__":
    main()        