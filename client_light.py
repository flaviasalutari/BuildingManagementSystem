import paho.mqtt.client as mqtt #Library for mqtt communication
import json # Library for handling json string
from controllight import ControlLight
from controllight import timesleep
import sys # Library to handle system exception
from home import Home
import time
# import MySQLdb # Library to handle the Database
from fileconfig import *

casa = Home("",obj_email) #Create the instance of the Home class to handle the various operation

#CONNESSIONE AL BROKER

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc)) 	# Show the connection result
	client.subscribe("#") 							# Perform the subscription on every topic

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload)) # Print the messages coming from the broker for every topic

# def response_callback(client, userdata, msg):
# 	casa.ParseResponse(client, msg.payload)

# def conf_callback(client, userdata, msg):
# 	casa.ParseConfiguration(client, msg.payload)

def State_callback(client, userdata, msg):
	casa.actuator(client, msg.payload)

# def Listen_callback(client, userdata, msg):
# 	casa.listen(client,msg.payload)

def main():
	# try:
	# 	db = MySQLdb.connect(hostdB,usernamedB,passworddB,dBname) #Connect to the database to retrieve the rooms already saved
	# 	cursor = db.cursor()
	# 	email = "'"+casa.email_owner+"'"
	# 	sql = "SELECT * from rooms where rooms.light =1 AND User_cod_user = (SELECT cod_user FROM user WHERE email=%s)" % email # The query search for rooms that have the subscription on light services
	# 	cursor.execute(sql)
	# 	for j in range(cursor.rowcount): # If there are rooms, they are added to the Home instance that will handle the operations to be done
	# 		data = cursor.fetchone()
	# 		casa.AddRoom(data[1],data[4],data[6],data[7],data[8],data[9], data[5]) # Add the room in the instance
	# 	db.close()
	# except:
	# 	sys.exit("Connection to the database failed")
	
	try:
		client = mqtt.Client()             	  # Create the client mqtt instance to send and retrieve messages to and from the broker 
		client.connect(IPbroker, 1883, 60) 	  # Connection of the mqtt client instance to the broker (in our case the raspberry)
		client.on_connect = on_connect        # Call the function to show the connection result
		client.on_message = on_message        # Call the function to print the message coming from the broker
		client.loop_start() 			      # Enter in the loop state the mqtt client connection

		#List of callback function
		# client.message_callback_add(str(casa.code_owner) + "/Configuration", conf_callback) 		# This topic is used to retrieve all messages coming from the web aplication
		# client.message_callback_add(str(casa.code_owner) + "/+/Light/Response", response_callback) 	# This topic is used to retrieve the time passed since last movement perceived by the PIR sensor, to switch off the light for profile 2 and 3
		# client.message_callback_add(str(casa.code_owner) + "/+/Light/Observe", Listen_callback)		# This topic is used to retrieve the message about an eventual motion perceived by the PIR sensor for profile 3
		client.message_callback_add(str(casa.code_owner) + "/+/Light/State", State_callback)		# This topic is used to retrieve all the changes of light on/off- ACK from Arduino
	except:
		sys.exit("Connection to the broker failed")
	
	#Starts the infinite loop that check the eventual operations to perform for every room
	while (1):
		# if casa.nRooms>0: 
		# 	i=0
			# print "------------"
			# print "Number of rooms: " + str(casa.nRooms)
			# while i< len(casa.ControlLight):
			# 	casa.handleRoom(i,client) # Check the operation to perform for the room
				# Show some detail about the rooms
				# print "- - -"
				# print "Room number: " + str(i)
				# print "Room name: " + casa.ControlLight[i].id
				# print "Profile: " + str(casa.ControlLight[i].profile)
				# print "State: " + str(casa.ControlLight[i].lighton)
		# 	  	i=i+1
		# else:
	 # 		pass
	 	time.sleep(timesleep)

if __name__ == "__main__":
	main()
