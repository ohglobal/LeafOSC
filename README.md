# LeafOSC
This program establishes a bidirectional OSC interface with Nanoleaf lighting instruments

## About
Nanoleaf lighting instruments, including Aurora Light Panels (the classic triangles) and Canvas (the squares) have a REST API. The python library "nanoleafapi" wraps the API for use in python code. This project uses this library to bridge the Nanoleaf API to Open Sound Control (OSC) for easy UDP interfacing from hardware, media servers, StreamDecks, etc. 

The link is bidirectional: OSC can be used to change the lights or to receive information about the lights.

## Commands to Send
/leafOSC/setPower - send a 1 to turn on the panels, send a 0 to turn them off (int 1,0)
/leafOSC/getPower - request a return packet with the current leaf power state (no args)
/leafOSC/togglePower - toggle the leaf power on or off (no args)
/leafOSC/setBrightness - set the brightness and the transition time (int brightness between 0-100, int transition_length)
/leafOSC/getBrightness - request a return packet with the current brightness of the leaves (no args)
/leafOSC/identify - flash the Nanoleaves (no args)
/leafOSC/setColorTemp - set the color temperature (int temp between 1200-6500)
/leafOSC/getColorTemp - request a return packet with the current color temperature of the Nanoleaves (no args)
/leafOSC/getCurrentEffect - request a return packet with the name of the current effect playing (no args)
/leafOSC/listAllEffects - request a return packet of the names of all the loaded effects (no args)
/leafOSC/setEffectByName - apply the effect with the provided name, if it exists (str name)
/leafOSC/setEffectByIndex - apply the effect at the index in the list provided, if it exists. REQUIRES RUNNING LIST FIRST (int index)
/leafOSC/makePulsate - create a pulsation of the r,g,b color over time t (int r,g,b,t where 0<=r,g,b<=255)
/leafOSC/makeFlow - create a flow of colors based on the provided string over time t (str cmd_string where format is progressive triplets of r,g,b as strings followed by int time, example: "255,0,0,0,255,0,0,0,255" 4 would cross from red to green to blue over 4 seconds
/leafOSC/makeSpectrum - cycle over the color spectrum over time t (int t)
/leafOSC/getPanelIDs - request a return and print all of the panel IDs (no args)
/leafOSC/getPanelColor - request a return of the color of the indicated panel (int panelID)
/leafOSC/setPanelColor - set the color of the panel with the id (int panelID OR -1 for all (distinct from setAllColor due to sync), int (int r,g,b where 0<=r,g,b<=255)
/leafOSC/sync - when autosync is off, this syncs the virtual controller with the lights (no args)
/leafOSC/setAutoSync - turn autosync on (1) or off (0) for live / buffered workflows (int 1,0)

## Commands to Receive
/leafOSC/powerState - the power state of the panels (int 1=on, 0=off)
/leafOSC/brightnessState - the brightness level of the panels (int)
/leafOSC/colorTempState - the color temperature of the panels (int)
/leafOSC/currentEffectName - the name of the active effect (string)
/leafOSC/effectList - list of string args for the names of effects (string list)
/leafOSC/panelIDs - list of the panel IDs (int list)
/leafOSC/panelColorState - color of the panel (int r,g,b)

## Known Issues
brightness command not working
color temp not working

