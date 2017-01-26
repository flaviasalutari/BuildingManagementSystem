import random
from fileconfig import *
import json
import time
from datetime import datetime


class SensorIntensity(): # Si trova all'esterno, il suo valore e letto dallo shadowing system
    
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self.topic = str(self.name) + "/Intensity"

    def sense_intensity(self, intensity):
        intensity = intensity + random.uniform(0,1)*0.05 # random rumore
        msg = {"sensor_type": "intensity","name": self.name,"intensity_sensed": intensity, "timestamp": str(datetime.now())}
        self.client.publish(self.topic, json.dumps(msg))

class SensorFlux(): # Si trova sopra la scrivania , nella colonna dei sensori. e letto dall artificial light

    def __init__(self, name,client):
        self.name = name
        self.client = client
        self.topic = str(self.name) + "/Flux"

        
    def sense_flux(self, shadowing_system, artificial_light, flux):
        self.lumen_lamp=artificial_light.lumen_lamp
        self.active_lamps= artificial_light.active_lamps
        self.external_flux = flux

        artificial_flux = self.active_lamps * self.lumen_lamp
        tint=shadowing_system.tint
        transmitted_flux = shadowing_system.perc_tints[tint]*self.external_flux
        total_flux = transmitted_flux + artificial_flux
        msg = {"sensor_type": "flux","name": self.name, "total_flux_sensed": total_flux, "timestamp": str(datetime.now())}
        self.client.publish(self.topic, json.dumps(msg))

           
class SensorPersonCounter():
    
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self.topic = str(self.name) + "/NPeople"

        
    def sense_person(self, n_people):
        msg = {"sensor_type": "PIR","name": self.name, "n_people_sensed": n_people, "timestamp": str(datetime.now())}
        self.client.publish(self.topic, json.dumps(msg))


        
from environment import Environment
import paho.mqtt.client as mqtt       
from controllers import ShadowingSystem, ArtificialLight

shadow_system = ShadowingSystem(default_tint,threshold)
artificial_light = ArtificialLight(required_flux, lumen_lamp, total_lamps)
outside_environment = Environment() # ricordati di assicurarti di essere nella stagione giusta

def main():
    

    try:
        client = mqtt.Client()             	  # Create the client mqtt instance to send and retrieve messages to and from the broker 
        client.connect(IPbroker, 1883, 60) 
        client.loop_start() 			  # Enter in the loop state the mqtt client connection

    except:
        sys.exit("Connection to the broker failed")
    
    
    sensore_intensity = SensorIntensity("sensore_intensity", client)
    sensore_flusso = SensorFlux("sensore_flusso", client)
    sensore_pir = SensorPersonCounter("sensore_PIR", client)
    
    while(1): 
        outside_environment.run_environment()
        sensore_intensity.sense_intensity(outside_environment.intensity)
        
        print "\n"
        time.sleep(4)

        sensore_flusso.sense_flux(shadow_system, artificial_light, outside_environment.flux)
        
        print "\n"
        time.sleep(4)

        sensore_pir.sense_person(outside_environment.n_people)
        
        print "\n"
    
        
        time.sleep(4)
    
    
    
if __name__ == "__main__":
    main()        