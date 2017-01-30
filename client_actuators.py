import paho.mqtt.client as mqtt
from environment import Environment
import sys
import time
from configuration_file import configuration_broker
from sensors import SensorIntensity, SensorFlux, SensorPersonCounter
from controllers import ShadowingSystem, ArtificialLight, ControlAirQuality



shadow_system = ShadowingSystem()
artificial_light = ArtificialLight()
air_quality_controller = ControlAirQuality()
outside_environment = Environment() # ricordati di assicurarti di essere nella stagione giusta

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))    # Show the connection result
    client.subscribe("#")                           # Perform the subscription on every topic

def on_message(client, userdata, msg):
   print(msg.topic+" "+str(msg.payload)) # Print the messages coming from the broker for every topic

def Intensity_callback(client, userdata, msg):
    shadow_system.read_msg(msg.payload)

def Flux_callback(client, userdata, msg):
    artificial_light.read_msg(msg.payload)
    
def NPeople_callback(client, userdata, msg):
    artificial_light.read_msg(msg.payload)
    air_quality_controller.read_msg(msg.payload)  
    shadow_system.read_msg(msg.payload)


def main():
   
    try:
        client = mqtt.Client()             	  # Create the client mqtt instance to send and retrieve messages to and from the broker 
        client.connect("localhost", 1883, 60) 	  # Connection of the mqtt client instance to the broker (in our case the raspberry)
        client.on_connect = on_connect        # Call the function to show the connection result
#        client.on_message = on_message        # Call the function to print the message coming from the broker
        client.message_callback_add("+/Intensity", Intensity_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.message_callback_add("+/Flux", Flux_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        # client.message_callback_add("+/NPeople", Art_Light_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        # client.message_callback_add("+/NPeople", Shadow_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.message_callback_add("+/NPeople", NPeople_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.loop_start() 			  # Enter in the loop state the mqtt client connection

    except:
        sys.exit("Connection to the broker failed")

    while(1): 
        shadow_system.request_msg_intensity(client)
        time.sleep(1)
        shadow_system.request_msg_people(client)
        time.sleep(1)

        artificial_light.request_msg_flux(client, shadow_system.perc_tints[shadow_system.tint])
        time.sleep(1)
        artificial_light.request_msg_people(client)
        time.sleep(1)

        air_quality_controller.request_msg_people(client)
        time.sleep(1)

#        time.sleep(5)



        
  
    
if __name__ == "__main__":
    main()