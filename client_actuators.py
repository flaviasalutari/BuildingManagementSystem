import paho.mqtt.client as mqtt
from environment import Environment
import sys
import time
from configuration_file import configuration_broker
from sensors import SensorIntensity, SensorFlux, SensorPersonCounter
from controllers import ShadowingSystem, LightController, ControlAirQuality
import dweetIO

from six.moves import urllib


shadow_system = ShadowingSystem()
light_controller = LightController()
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
    light_controller.read_msg(msg.payload)
    
def NPeople_callback(client, userdata, msg):
    light_controller.read_msg(msg.payload)
    air_quality_controller.read_msg(msg.payload)  
    shadow_system.read_msg(msg.payload)


# def dweet_sensor_params(shadow_system, light_controller, air_quality_controller):
#     dweetIo= "https://dweet.io/dweet/for/"
#     my_thing = "sensors_parameters" 
#     flux = str(light_controller.total_flux)
#     intensity = str(shadow_system.ex_intensity)
#     n_people = str(air_quality_controller.n_people)
#     url = dweetIo + my_thing + "?" + "flux" + "=" + flux  + "&" + "intensity" + "=" + intensity + "&" + "n_people" + "=" + n_people
#     urllib.request.urlopen(url)

# def dweet_actuators_params(shadow_system, air_quality_controller):
#     dweetIo= "https://dweet.io/dweet/for/"
#     my_thing = "actuators_parameters" 
#     if air_quality_controller.ACH == 0:
#         VOC = str(0)
#     else:
#         VOC=str((1.0*air_quality_controller.voc_numerator)/air_quality_controller.ACH)
#     tint = str(shadow_system.tint)
#     url = dweetIo + my_thing + "?" + "VOC" + "=" + VOC  + "&" + "tint" + "=" + tint
#     urllib.request.urlopen(url)

# def dweet_light_control(light_controller):
#     dweetIo= "https://dweet.io/dweet/for/"
#     my_thing = "light_control" 
#     d_light=str(light_controller.active_lamps_desk)

#     # showing which ambients are active
#     am_light_1=str(0)
#     am_light_2=str(0)
#     am_light_3=str(0)
#     if light_controller.active_ambients == 1:
#         am_light_1=str(1)
#     elif light_controller.active_ambients == 2:
#         am_light_1=str(1)
#         am_light_2=str(1)
#     elif light_controller.active_ambients == 3:
#         am_light_1=str(1)
#         am_light_2=str(1)
#         am_light_3=str(1)

#     my_thing2= "lumens"
#     lumen_desk=str(int(light_controller.total_lamps_desk * light_controller.lumen_lamp_desk))+"lm"
#     lumen_ambient=str(int(light_controller.lamps_per_ambient*light_controller.lumen_lamp_ambient))+"lm"
#     url = dweetIo + my_thing + "?" + "d_light" + "=" + d_light + "&" + "am_light_1" + "=" + am_light_1 + "&" + "am_light_2" + "=" + am_light_2 + "&" + "am_light_3" + "=" + am_light_3 
#     url2 = dweetIo + my_thing2 + "?" + "lumen_desk" + "=" + lumen_desk + "&" + "lumen_ambient" + "=" + lumen_ambient
#     urllib.request.urlopen(url)
#     urllib.request.urlopen(url2)

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

        light_controller.request_msg_flux(client, shadow_system.perc_tints[shadow_system.tint])
        time.sleep(1)
        light_controller.request_msg_people(client)
        time.sleep(1)

        air_quality_controller.request_msg_people(client)
        time.sleep(1)

        dweetIO.dweet_sensor_params(shadow_system, light_controller, air_quality_controller)
        dweetIO.dweet_actuators_params(shadow_system, air_quality_controller)
        dweetIO.dweet_light_control(light_controller)
        dweetIO.dweet_datetime()
#        time.sleep(5)
        
        
  
    
if __name__ == "__main__":
    main()