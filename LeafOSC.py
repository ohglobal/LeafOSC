#	LeafOSC
#	A program for controlling NanoLeaf lighting via Open Sound Control (OSC)
#	Office Hours Global Community Project
#	Created and maintained by Andy Carluccio - Washington, D.C.

#import the nanoleaf pythong library (API wrapper)
from nanoleafapi import Nanoleaf, NanoleafDigitalTwin

#system
import sys

#OSC variables & libraries
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client 
from pythonosc import osc_bundle
from pythonosc import osc_bundle_builder

#Argument management
import argparse

#Nanoleaf API Objects
nl = None
nldt = None

effects = []
autoSync = True

#OSC API Functions-----------------------------------

def setPower(unused_addr, state):
	print("Received Power Set Command")
	if(state == 0):
		#turn off leaves
		nl.power_off()
	elif (state == 1):
		#turn on leaves
		nl.power_on()   

def getPower(unused_addr):
	print("Received Request for Power State")
	power_state = nl.get_power()
	print(power_state)
	if(power_state):
		client.send_message("/leafOSC/powerState", 1)
	else:
		client.send_message("/leafOSC/powerState", 0)

def togglePower(unused_addr):
	print("Received Power Toggle Command")
	nl.toggle_power()

def setBrightness(unused_addr, brightness, durration):
	print("Received Set Brightness Command")
	if(brightness > 100 or brightness < 0):
		print("Out of range 0-100")
	else:
		nl.set_brightness(brightness,durration)

def getBrightness(unused_addr):
	print("Received Request for Brightness State")
	brightness = nl.get_brightness()
	print(brightness)
	client.send_message("/leafOSC/brightnessState", brightness)

def identify(unused_addr):
	print("Received Identify Command")
	print("Nanoleaves are now blinking...")
	nl.identify()

def setColorTemp(unused_addr, temp):
	print("Received Color Temp Set Command")
	nl.set_color_temp(temp)

def getColorTemp(unused_addr):
	print("Received Request for Color Temp State")
	temp = nl.get_color_temp()
	print(temp)
	client.send_message("/leafOSC/colorTempState", temp)

def getCurrentEffect(unused_addr):
	print("Received Request for Current Effect Name")
	name = nl.get_current_effect()
	print(name)
	client.send_message("/leafOSC/currentEffectName", name)

def listAllEffects(unused_addr):
	global effects
	print("Received Request for List of all Effects")
	effects = nl.list_effects()

	#Send the list to OSC 
	osc_address = "/leafOSC/effectsList"
	bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
	msg = osc_message_builder.OscMessageBuilder(address=osc_address)

	for x in range (0,len(effects)):
		msg.add_arg(str(effects[x]))
		bundle.add_content(msg.build())
		print((str(effects[x])))

	bundle = bundle.build()
	client.send(bundle)

def setEffectByName(unused_addr, name):
	print("Received Command to set Effect by Name")
	nl.set_effect(name)

def setEffectByIndex(unused_addr, index):
	print("Received Command to set Effect by Index")
	if(index < len(effects) and index >= 0):
		nl.set_effect(effects[index])
		print(effects[index])
	else:
		print("Index out of range")

def makePulsate(unused_addr,r,g,b,t):
	print("Received Command to Create Pulsation Effect")
	nl.pulsate((int(r),int(g),int(b)),t)

def makeFlow(unused_addr,flow_string,t):
	print("Received Command to Create Flow Effect")
	colors = flow_string.split(",")
	if(len(colors)%3 != 0):
		print("Invalid color flow string")
		return

	color_array = []
	x=0
	while(x<len(colors)):
		r = int(colors[x])
		g = int(colors[x+1])
		b = int(colors[x+2])
		color = [r,g,b]
		color_array.append(color)
		x = x + 3

	nl.flow(color_array,t)

def makeSpectrum(unused_addr,t):
	print("Received Command to Create Spectrum Cycle Effect")
	nl.spectrum(t)

def getPanelIDs(unused_addr):
	print("Received Request for Panel ID List")
	ids = nldt.get_ids()
	
	#Send the list to OSC 
	osc_address = "/leafOSC/panelIDs"
	bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
	msg = osc_message_builder.OscMessageBuilder(address=osc_address)

	for x in range (0,len(ids)):
		msg.add_arg(int(ids[x]))
		bundle.add_content(msg.build())
		print((int(ids[x])))

	bundle = bundle.build()
	client.send(bundle)


def setPanelColor(unused_addr,panel_id,r,g,b):
	print("Received Command to Set Panel Color")
	if(panel_id == -1):
		nldt.set_all_colors((r,g,b))
	else:
		nldt.set_color(panel_id,(r,g,b))

	if(autoSync):
		nldt.sync()

def getPanelColor(unused_addr, panel_id):
	print("Received Request for a Panel's Color")
	c = nldt.get_color(panel_id)

	#Send the list to OSC 
	osc_address = "/leafOSC/panelColorState"
	bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
	msg = osc_message_builder.OscMessageBuilder(address=osc_address)

	for x in range (0,len(c)):
		msg.add_arg(int(c[x]))
		bundle.add_content(msg.build())
		print((int(c[x])))

	bundle = bundle.build()
	client.send(bundle)

def setAllColor(unused_addr, r,g,b):
	print("Received Color Set Command")
	nl.set_color((r,g,b))

def sync(unused_addr):
	print("Received Sync Command")
	nldt.sync()

def setAutoSync(unused_addr, set):
	print("Received Auto-Sync Set Command")
	global autoSync
	if(set==1):
		autoSync = True;
	elif(set==0):
		autoSync = False;


#Main execution script--------------------------------------
if __name__ == "__main__":

	#Greeting
	print("Welcome to LeafOSC")
	print("Created by Andy Carluccio")
	print("This program establishes a bidirectional OSC interface with Nanoleaf")
	print("See ReadMe for commands and useage")
	print()
	
	#get the IP of the leaf controller
	leafIP = "192.168.1.203"
	print("Would you like to [1] enter the IP address of the Nanoleaves or [2] use default 192.168.1.203 \n")
	sl = int(input())
	if(sl == 1):
		leafIP = str(input("Nanoleaf IP?: \n"))
	else:
		print("Using default Nanoleaf settings")

	#OSC Setup
	print("Would you like to [1] Input network parameters or [2] use default: 127.0.0.1:1234 (sending) :7050 (receiving)")
	
	send_ip = "127.0.0.1"
	send_port = 1234
	receive_port = 7050

	selection = int(input())
	if(selection == 1):
		print("Input network parameters")
		send_ip = str(input("Send ip?: "))
		send_port = int(input("Send port?: "))
		receive_port = int(input("Receive port?: "))
	else:
		print("Using default network settings")

	#create the osc sending client
	client = udp_client.SimpleUDPClient(send_ip,send_port)

	#catches OSC messages
	dispatcher = dispatcher.Dispatcher()

	#map functions here:
	dispatcher.map("/leafOSC/setPower", setPower)
	dispatcher.map("/leafOSC/getPower", getPower)
	dispatcher.map("/leafOSC/togglePower", togglePower)
	dispatcher.map("/leafOSC/setBrightness", setBrightness)
	dispatcher.map("/leafOSC/getBrightness", getBrightness)
	dispatcher.map("/leafOSC/identify", identify)
	dispatcher.map("/leafOSC/setColorTemp", setColorTemp)
	dispatcher.map("/leafOSC/getColorTemp", getColorTemp)
	dispatcher.map("/leafOSC/getCurrentEffect", getCurrentEffect)
	dispatcher.map("/leafOSC/listAllEffects", listAllEffects)
	dispatcher.map("/leafOSC/setEffectByName", setEffectByName)
	dispatcher.map("/leafOSC/setEffectByIndex", setEffectByIndex)
	dispatcher.map("/leafOSC/makePulsate", makePulsate)
	dispatcher.map("/leafOSC/makeFlow", makeFlow)
	dispatcher.map("/leafOSC/makeSpectrum", makeSpectrum)
	dispatcher.map("/leafOSC/getPanelIDs", getPanelIDs)
	dispatcher.map("/leafOSC/setPanelColor", setPanelColor)
	dispatcher.map("/leafOSC/getPanelColor", getPanelColor)
	dispatcher.map("/leafOSC/setAllColor", setAllColor)
	dispatcher.map("/leafOSC/sync", sync)
	dispatcher.map("/leafOSC/setAutoSync", setAutoSync)

	#set up server to listen for osc messages
	server = osc_server.ThreadingOSCUDPServer((send_ip,receive_port),dispatcher)

	#Print the info
	sys.stdout.write("Opened Client on: ")
	sys.stdout.write(send_ip)
	sys.stdout.write(":")
	sys.stdout.write(str(send_port))
	sys.stdout.write('\n')
	sys.stdout.write("Listening on: ")
	sys.stdout.write(str(receive_port))
	sys.stdout.write('\n')

	print()

	#Nanoleaf Object init
	nl = Nanoleaf(leafIP)
	nldt = NanoleafDigitalTwin(nl)

	#begin the infinite loop
	server.serve_forever()
