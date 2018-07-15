#!/usr/bin/env python3
# using NeoPixel library and LCD screen library  
# Tony DiCola (tony@tonydicola.com)
# https://learn.adafruit.com/nokia-5110-3310-lcd-python-library/overview
# And a simple stepper motor by Matt Hawkins
# http://flipmytext.com/ascii/                            
#     o  __ __   __   __   __  _|_  
#     | |  )  ) |__) (__) |  '  |_, 
#               |                     
#____________________________________________
import os
import glob
from time import sleep
import threading
import argparse
import sys 
import RPi.GPIO as GPIO #GPIO 
from PIL import Image	#image reader
#NEOPIXEL
sys.path.append('home/pi/rpi_ws281x/python')
from neopixel import *
#LCD screen
sys.path.append('/home/pi/Adafruit_Nokia_LCD/Adafruit_Nokia_LCD')
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
#----------------------------------------------------
	
#****************************************************
#****************************************************
#***                                  _           ***                                      
#***  __  ___  _|_         __       _|_  __   __  ***
#***__)  (__/_  |_, (__(_ |__)       |  (__( |  ) ***
#***                      |                       ***        
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT) 
GPIO.setup(25, GPIO.OUT) 
fan_list = (12,25) #GPIO pins 12 and 25
GPIO.output(fan_list, GPIO.LOW) # all LOW
#  _                             
#_|_        __  _|_  o  __   __  
# |  (__(_ |  )  |_, | (__) |  ) 
def fan(direction): #spin the fan 
	
	if (120<=direction<=130): #CW (green)
		spin_the_fan (25)
		print " fan %i" %(direction)	
	elif (230<=direction<=255):#CCW (red)
  		spin_the_fan (12)
  		print " fan %i" %(direction)	
  	else: 
		GPIO.output(fan_list, GPIO.LOW) # all LOW
		

def spin_the_fan (_fan_pin):
	#GPIO.output(_fan_pin, 1)
	#sleep(.5)
	#GPIO.output(_fan_pin, 0)
	GPIO.output(_fan_pin, 1)
	sleep(0.005)
	GPIO.output(_fan_pin, 0)
	sleep(0.08)
	
	GPIO.output(_fan_pin,1)
	sleep(0.007)
	GPIO.output(_fan_pin,0)
	sleep(0.08)
	
	GPIO.output(_fan_pin, 1)
	sleep(0.005)
	GPIO.output(_fan_pin, 0)
	sleep(0.1)
	
	GPIO.output(_fan_pin,1)
	sleep(0.007)
	GPIO.output(_fan_pin,0)
	
	
	
#--------------------------------------------------------------------------
	




#**************************************************************************	
#**************************************************************************
#***  __  ___  _|_         __       __   ___   __   __  o \_'  ___  |   ***
#***__)  (__/_  |_, (__(_ |__)     |  ) (__/_ (__) |__) | / \ (__/_ |_, ***
#***                      |                        |                    ***
LEDCOUNT      = 4      # Number of LED pixels.
GPIOPIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
FREQ    = 800000  # LED signal frequency in hertz (usually 800khz)
DMA        = 10      # DMA channel to use for generating signal (try 10)
BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = Adafruit_NeoPixel(LEDCOUNT, GPIOPIN, FREQ, DMA, INVERT, BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()
#--------------------------------------------------------------------------
	




#******************************************************
#******************************************************                                     
#***  __  ___  _|_         __      |    __   __| 	***
#***__)  (__/_  |_, (__(_ |__)     |_, (___ (__| 	***
#***                      |                      	***

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Initialize library.
disp.begin(contrast=40)

# Clear display.
disp.clear()
disp.display()

#  _                             
#_|_        __  _|_  o  __   __  
# |  (__(_ |  )  |_, | (__) |  ) 

def videoLCD(frame_number,tikker):
	if (tikker>240):
		    
			countedfiles = 0
			current_frame= frame_number-91
			print " VIDEO %i" %(tikker)
			for infile in sorted(glob.glob('smoke/asmoke/*')):
				if (countedfiles == current_frame):
					image = Image.open(infile).convert('1')
					disp.image(image)
					disp.display()
				countedfiles += 1

#--------------------------------------------------------------------------
	




#**********************************************************************************
#**********************************************************************************  
#***                                                                            ***
#***     __  ___  _|_         __        __ _|_   ___   __   __   ___   __    __ ***    
#***   __)  (__/_  |_, (__(_ |__)     __)   |_, (__/_ |__) |__) (__/_ |  ' __)  ***    
#***                         |                        |    |                    ***


StepPinsLEFT = [5,17,22,27]	#GPIO pins in use
StepPinsRIGHT = [16,6,26,13]

# Set the pins as output
for pin in StepPinsLEFT:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
for pin in StepPinsRIGHT:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
StepSequence = [[0,0,0,1],
				[0,0,1,0],
				[0,1,0,0],
				[1,0,0,0]] 
StopSequence = [[0,0,0,0]]				
				
#variables
			
Wait_Time = 8/float(1000)

#  _                             
#_|_        __  _|_  o  __   __  
# |  (__(_ |  )  |_, | (__) |  ) 


def stepper(ticker,_Photodata):
		#print " stepeper@ %i" %(_Photodata)
		#_Photodata = 107
		#variables
		StepDirection = 0
		Motor = 0
		# decide  what direction
		RGB = photodata.getpixel((ticker,(_Photodata+1))) 
		R,G,B = RGB  #now you can use the RGB value
		if (240<=R<=255):
			StepDirection=1 #CW (green)CCW #PUSH
				
		RGB = photodata.getpixel((ticker,(_Photodata-1))) 
		R,G,B = RGB  #now you can use the RGB value
		if (240<=R<=255):
			StepDirection=-1 #CW (green)CCW #PUll
		
		#decide which motor

		if (_Photodata == photodata_stepR):
			StepPins=StepPinsRIGHT
			Motor = 8
			
		else:
			StepPins=StepPinsLEFT
			Motor = 4
		
		SSQ=StepSequence
		
		#if 	(StepDirection != -1 or StepDirection != 1):
			#print " Stop GPIO" 
			#SSQ=StopSequence
			#StepCount = 1
			
		StepCount = len(StepSequence)	
		StepCounter = 0
			
		#print " Enable GPIO %i. %i " %(StepDirection,Motor) 
		
		  

		for sequenceRuns in range(0, 50): #amount of times the squence runs in one frame
		  
		  #print StepCounter,
		  #print SSQ[StepCounter]
		  
		  for pin in range(0,4):
				xpin = StepPins[pin]
				if SSQ[StepCounter][pin]!=0:
				  #print " Enable GPIO %i" %(xpin)
				  GPIO.output(xpin, True)
				else:
				  GPIO.output(xpin, False)
		  StepCounter += StepDirection
	 
		  # If we reach the end of the sequence
		  # start again
		  if (StepCounter>=StepCount):
			StepCounter = 0
		  if (StepCounter<0):
			StepCounter = StepCount+StepDirection
			
			# Wait before moving on
		  sleep(Wait_Time)

#--------------------------------------------------------------------------

#**********************************************************************************
#**********************************************************************************  
#***                                                                            ***                                                                            
#***  __  ___  _|_         __       __  |__   __  _|_   __   __|  __  _|_   __  *** 
#***__)  (__/_  |_, (__(_ |__)     |__) |  ) (__)  |_, (__) (__| (__(  |_, (__( *** 
#***                      |        |                                            *** 
#***																			*** 


photodata = Image.open('timepath.png') #your image
#photodata = photodata.convert('RGB')

timeline = photodata.size[0] #define W and H
height = photodata.size[1]
#ticker timers on the timeline
photodata_BottomLED = 5
photodata_TopLED = 15
photodata_StartLCD =25
photodata_EndLCD =35
photodata_fan =40
photodata_asmoke = 45
photodata_bsmoke = 45+(5*1)
photodata_csmoke = 45+(5*2)
photodata_dsmoke = 45+(5*3)
photodata_esmoke = 45+(5*4)
photodata_fsmoke = 45+(5*5)
photodata_ismoke = 45+(5*6)
photodata_jsmoke = 45+(5*7)
photodata_ksmoke = 45+(5*8)
photodata_stepR = 106
photodata_stepL = 120

#--------------------------------------------------------------------------

# Describe your threading function...
#def threading_fan():
#  fan()

 



#thread = threading.Thread(target= threading_fan)
#thread.start()


##################################################################
### _____   _____       ___   _____    _____   _   _   _____  ####
###/  ___/ |_   _|     /   | |  _  \  |_   _| | | | | |  _  \ ####
###| |___    | |      / /| | | |_| |    | |   | | | | | |_| | ####
###\___  \   | |     / / | | |  _  /    | |   | | | | |  ___/ ####
### ___| |   | |    / /  | | | | \ \    | |   | |_| | | |     ####
###/_____/   |_|   /_/   |_| |_|  \_\   |_|   \_____/ |_|     ####
##################################################################


# First LED white
strip.setPixelColor(0, Color(1,1,1))
strip.setPixelColor(1, Color(1,1,1))
strip.setPixelColor(2, Color(1,1,1))
strip.setPixelColor(3, Color(1,1,1))
 
strip.show()

# fan



for dothisloopXtimes in range(0, 100):

	for x in range(0, timeline):

		RGB = photodata.getpixel((x,photodata_BottomLED))
		R,G,B = RGB  #now you can use the RGB value
		strip.setPixelColor(0, Color(R,G,B))
				
		RGB = photodata.getpixel((x,photodata_TopLED))
		R,G,B = RGB  #now you can use the RGB value
		strip.setPixelColor(1, Color(R,G,B))
				
		RGB = photodata.getpixel((x,photodata_StartLCD))
		R,G,B = RGB  #now you can use the RGB value
		strip.setPixelColor(2, Color(R,G,B))

		RGB = photodata.getpixel((x,photodata_EndLCD))
		R,G,B = RGB  #now you can use the RGB value
		strip.setPixelColor(3, Color(R,G,B))
		strip.show()
		
		RGB = photodata.getpixel((x,photodata_fan)) #fan
		R,G,B = RGB  #now you can use the RGB value
		fan(R)
		
		RGB = photodata.getpixel((x,photodata_asmoke)) #video
		R,G,B = RGB  #now you can use the RGB value
		if (R>200): 
			videoLCD(x,200)
		
		RGB = photodata.getpixel((x,photodata_stepR)) #stepperR
		R,G,B = RGB  #now you can use the RGB value
		#if (R != 0 ):
			 #stepper(x,photodata_stepR)
		
		RGB = photodata.getpixel((x,photodata_stepL)) #stepperL
		R,G,B = RGB  #now you can use the RGB value
		#if (R != 0 ):
			 #stepper(x,photodata_stepL)
		#print " Frame %i" %(x)
		
		sleep(0.125)		


GPIO.cleanup()
print('exit')
		


