# BuildingManagementSystem
**List of Python Modules:

 * client_controllers.py  	# main of the controllers
 * client_sensors.py 		# main of the sensors

 - configurationbroker.py 	# configuration file with broker parameters
 - configurationenvironment.py 	# configuration file with environment parameters
 - configurationroom.py 	# configuration file with parameters of the room

 - environment.py 		# class containing the functions for generating environmental parameters

 - sensorflux.py 		# flux sensor
 - sensorintensity.py		# intensity sensor
 - peoplecounter.py 		# people counter sensor

 - controlairquality.py		# class of the Air Quality controller
 - shadowingsystem.py		# class of the Shading System
 - lightcontroller.py 		# class of the Artificial Light controller
 
 - script_freeboard.py 		# script that must run in order to use Freeboard
 - dweetIO.py 			# list of functions for graphical interface (Dweet and Freeboard)



Usage:

Run in parallel the following modules in this order:
 1. script_freeboard.py
 2. client_sensors.py
 3. client_controllers.py

The main parameters are shown in real time at this link:
 https://freeboard.io/board/XY7qMD
