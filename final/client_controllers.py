# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from environment import Environment
import sys
import time
from configurationbroker import configuration_broker
from shadingsystem import ShadingSystem
from lightcontroller import LightController
from controlairquality import ControlAirQuality
import dweetIO

shadow_system = ShadingSystem() # initialize shading system
light_controller = LightController() # initialize light controller
air_quality_controller = ControlAirQuality() # initialize air quality monitoring system
# outside_environment = Environment() # initialize environment, external parameters generator

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))    # Show the connection result
    client.subscribe("#")                           # Perform the subscription on every topic

def on_message(client, userdata, msg):
   print(msg.topic+" "+str(msg.payload)) # Print the messages coming from the broker for every topic

def Intensity_callback(client, userdata, msg):
    shadow_system.read_msg(msg.payload)   # shading system parse msgs coming from intensity sensor

def Flux_callback(client, userdata, msg):
    light_controller.read_msg(msg.payload) # light controller parse msgs coming from flux sensor
    
def NPeople_callback(client, userdata, msg):
    light_controller.read_msg(msg.payload)  # light controller parse msgs coming from people counter sensor    
    air_quality_controller.read_msg(msg.payload)  # air quality controller parse msgs coming from people counter sensor
    # shadow_system.read_msg(msg.payload) # shading system controller parse msgs coming from people counter sensor


def main():
   
    try:
        client = mqtt.Client("Controllers")   # Create the client mqtt instance to send and retrieve messages to and from the broker 
        client.connect(configuration_broker["IPbroker"], configuration_broker["port"], 60)  # Connection of the mqtt client instance to the broker
        client.on_connect = on_connect  # Call the function to show the connection result
#        client.on_message = on_message        # Call the function to print the message coming from the broker
        client.message_callback_add("+/Intensity", Intensity_callback) # This topic is used to retrieve values sensed by intensity sensor
        client.message_callback_add("+/Flux", Flux_callback) # This topic is used to retrieve all the values sensed by flux sensor
        client.message_callback_add("+/NPeople", NPeople_callback) # This topic is used to retrieve the number of people in the room
        client.loop_start() # Enter in the loop state the mqtt client connection

    except:
        sys.exit("Connection to the broker failed") # raise error in case of failed connection to the broker

    while(1): 
        shadow_system.request_msg_intensity(client) # shading system requests intensity value to the sensor
        time.sleep(1)
        # shadow_system.request_msg_people(client) # shading system requests number of people
        # time.sleep(1)

        light_controller.request_msg_flux(client, shadow_system.perc_tints[shadow_system.tint]) # light controller requests the flux value
                                                                                                # NB: shadow_system.perc_tints[shadow_system.tint]
                                                                                                #  is the transmittance factor of the tint in use
                                                                                                # it is passed in the function ONLY FOR THE SAKE
                                                                                                # OF SIMULATION!
        time.sleep(1)
        light_controller.request_msg_people(client)  # light controller requests the number of people in the room
        time.sleep(1)

        air_quality_controller.request_msg_people(client)  # the air quality controller requests the number of people in the room
        time.sleep(1)

        dweetIO.dweet_sensor_params(shadow_system, light_controller, air_quality_controller) # publish values on dweet
        dweetIO.dweet_actuators_params(shadow_system, air_quality_controller)# publish values on dweet
        dweetIO.dweet_light_control(light_controller) # publish values on dweet
        dweetIO.dweet_datetime() # publish hour in datetime format on dweet
#        time.sleep(5)      
  
    
if __name__ == "__main__":
    main()