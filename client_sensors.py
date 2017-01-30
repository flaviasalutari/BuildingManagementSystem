import time
import sys        
from environment import Environment
import paho.mqtt.client as mqtt   
from configuration_file import configuration_broker    
from sensors import SensorIntensity, SensorFlux, SensorPersonCounter
#



outside_environment = Environment()
outside_environment.run_environment()

sensore_intensity = SensorIntensity("sensore_intensity")
sensore_flusso = SensorFlux("sensore_flusso")
sensore_pir = SensorPersonCounter("sensore_PIR")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))    # Show the connection result
    client.subscribe("#")       

def Intensity_callback(client, userdata, msg):
    sensore_intensity.parse_msg(msg.payload, client, outside_environment.intensity)

def Flux_callback(client, userdata, msg):
    sensore_flusso.parse_msg(msg.payload, client, outside_environment.flux)
    
def Nperson_callback(client, userdata, msg):
    sensore_pir.parse_msg(msg.payload, client, outside_environment.n_people)    

def main():
    

    try:
        client = mqtt.Client()             	  # Create the client mqtt instance to send and retrieve messages to and from the broker 
        client.connect("localhost", 1883, 60) 	  # Connection of the mqtt client instance to the broker (in our case the raspberry)
        client.on_connect = on_connect        # Call the function to show the connection result        
        client.message_callback_add("+/GetIntensity", Intensity_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.message_callback_add("+/GetFlux", Flux_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.message_callback_add("+/GetNpeople", Nperson_callback) # This topic is used to retrieve all the changes of light on/off- ACK from Arduino
        client.loop_start()               # Enter in the loop state the mqtt client connection
    except:
        sys.exit("Connection to the broker failed")
    
    
    
    while(1): 
        outside_environment.run_environment()



        
    
    
if __name__ == "__main__":
    main()        