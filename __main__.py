import paho.mqtt.client as mqtt
from environment import Environment
import sys
import json
import time
from fileconfig import *
from sensors import SensorIntensity, SensorFlux, SensorPersonCounter
from controllers import ShadowingSystem, ArtificialLight

shadow_system = ShadowingSystem(default_tint,threshold)
artificial_light = ArtificialLight(required_flux, lumen_lamp, total_lamps)
outside_environment = Environment() # ricordati di assicurarti di essere nella stagione giusta

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))    # Show the connection result
    client.subscribe("#")                           # Perform the subscription on every topic
# 
#def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload)) # Print the messages coming from the broker for every topic

def Shadow_callback(client, userdata, msg):
    shadow_system.read_msg(msg.payload)

def Art_Light_callback(client, userdata, msg):
    artificial_light.read_msg(msg.payload)
    
def Out_Environ_callback(client, userdata, msg):
    outside_environment.read_msg(msg.payload)     
 
def main():

    
    try:
        client = mqtt.Client()             	  # Create the client mqtt instance to send and retrieve messages to and from the broker 
        client.connect(IPbroker, 1883, 60) 	  # Connection of the mqtt client instance to the broker (in our case the raspberry)
        client.on_connect = on_connect        # Call the function to show the connection result
#        client.on_message = on_message        # Call the function to print the message coming from the broker

        client.message_callback_add("+/Intensity", Shadow_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.message_callback_add("+/Flux", Art_Light_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.message_callback_add("+/NPeople", Out_Environ_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.message_callback_add("+/NPeople", Art_Light_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.loop_start() 			  # Enter in the loop state the mqtt client connection

    except:
        sys.exit("Connection to the broker failed")

    while(1): 

        pass

    
    
    
    
if __name__ == "__main__":
    main()