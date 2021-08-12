####################################
# PiDash Control Script
#####################################
# Hardware by Eladio Martinez
# http://mini-mods.com
#
#####################################
# Wiring:
#  GPIO4  Fan ON signal (OUTPUT)
#  GPIO14 LED (OUTPUT)
#  GPIO20 INFO_BTN (INPUT)
#
#####################################
#  Required libraries
#  sudo apt-get install python3-pip python3-pil python-smbus python-gpiozero i2c-tools
#  sudo pip3 install psutil pyserial adafruit-circuitpython-ssd1306
#
#####################################
# Basic Usage:
#  INFO_BTN Press
#	Display show system information, IP, CPU load and current temperature and system uptime 
#  INFO_BTN Hold 5 seconds
#	System will reboot
#  INFO_BTN Hold 10 seconds 
#	System wil soft-shutdown
#
#  FAN ON
#	Fan will turn ON when temperature exceeded 55C
#  FAN OFF
#	Fan will turn OFF when temperature under 40C


import time
import subprocess
import os

from board import SCL, SDA
import busio
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import psutil

##### Pin configuration #########

FAN_CRTL = 4
LED = 14
INFO_BTN = 15

################################

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_CRTL, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(INFO_BTN, GPIO.IN)

DISP_OFF = 0xAE

# Fan control settings
fan = GPIO.PWM(FAN_CRTL, 50) #PWM freauency set to 50Hz

#Turn off fan when under
minTEMP=40

#Turn on fan when exceeded
maxTEMP=55

# Timer for Display timeout
disp_timer = 0
DISP_TIMEOUT = 15

# Menu Variables
menu_state = 0 # 0 = Info; 1 = Reboot; 2 = Restart
menu_timer = 0
REBOOT_TIMEOUT = 5
SHUTDOWN_TIMEOUT = 10

do_reboot = 0
do_shutdown = 0

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.rotation = 2
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

#Get CPU Temperature
def getCPUtemp():
	res = os.popen('vcgencmd measure_temp').readline()
	return (res.replace("temp=","").replace("'C\n",""))

GPIO.output(LED, GPIO.HIGH)

# Startup Info
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x, top),    "-"*20, font=font, fill=255)
draw.text((x, top+12), "   System Started   ", font=font, fill=255)
draw.text((x, top+24), "-"*20, font=font, fill=255)
disp.image(image)
disp.show()

time.sleep(5)

while True:

    #Fan control
    #Adjust MIN and MAX TEMP as needed to keep the FAN from kicking
    #on and off with only a one second loop
    cpuTemp = int(float(getCPUtemp()))
    fanOnTemp = maxTEMP  #Turn on fan when exceeded
    fanOffTemp = minTEMP  #Turn off fan when under
    if cpuTemp >= fanOnTemp:
    	fan.start(90) #90% duty cycle
    if cpuTemp < fanOffTemp:
        fan.stop()

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # Info Button pressed?
    if GPIO.input(INFO_BTN) == 0:
        #if disp_timer == 0:
            # disp.begin()
        if menu_timer >= REBOOT_TIMEOUT:
            menu_state = 1
        if menu_timer >= SHUTDOWN_TIMEOUT:
            menu_state = 2
        disp_timer = DISP_TIMEOUT
        menu_timer = menu_timer+1
    elif disp_timer == 0:
        disp.image(image)
        disp.show()
        # disp.poweroff()
    
    if disp_timer > 0:

        if menu_state == 0:
            # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "hostname"
            HOSTNAME =  subprocess.check_output(cmd, shell = True)
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell = True)
            cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
            SysTemp = subprocess.check_output(cmd, shell = True)
            dskpct = psutil.disk_usage('/')
            disk = str(dskpct.percent)
            #cmd = "df -h | awk '$NF=="/"{printf "(%s)\n", $5}'"
            #disk = subprocess.check_output(cmd, shell = True).decode(UTF-8)
            
            # Examples of getting system information from psutil : https://www.thepythoncode.com/article/get-hardware-system-information-python#CPU_info
            CPU = "{:3.0f}".format(psutil.cpu_percent())
            svmem = psutil.virtual_memory()
            MemUsage = "{:2.0f}".format(svmem.percent)
            SysUpTime = os.popen('uptime -p').readline()


            draw.rectangle((0,0,width,height), outline=0, fill=0)
			
		
            draw.text((x, top),       "IP : " + IP.decode('UTF-8'),  font=font, fill=255)
            draw.text((x, top+12),    "CPU: " + CPU + "% @ " + SysTemp.decode('UTF-8'), font=font, fill=255)
            draw.text((x, top+24),    SysUpTime,  font=font, fill=255)
                      
            disp_timer =  disp_timer-1

            if GPIO.input(INFO_BTN) == 1:
                menu_timer = 0

        if menu_state == 1:
            if GPIO.input(INFO_BTN) == 1:
                do_reboot = 1
                draw.text((x, top+12), "Performing Reboot...", font=font, fill=255)
                disp.image(image)
                disp.show()
                time.sleep(3)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
            else:
                draw.text((x, top),    ".......Reboot......."     , font=font, fill=255)
                draw.text((x, top+12), "   Release Button   "   , font=font, fill=255)
                draw.text((x, top+24), "      To Reboot     "    , font=font, fill=255)

        if menu_state == 2:
            if GPIO.input(INFO_BTN) == 1:
                do_shutdown = 1
                draw.text((x, top+12), "Shutting down.......", font=font, fill=255)
                disp.image(image)
                disp.show()
                time.sleep(3)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
            else:
                draw.text((x, top),    "......Shutdown......"     , font=font, fill=255)
                draw.text((x, top+12), "   Release Button   "   , font=font, fill=255)
                draw.text((x, top+24), "    To Shutdown     "      , font=font, fill=255)

        disp.image(image)
        disp.show()

        if do_reboot == 1:
            cmd = "sudo reboot now"
            subprocess.Popen(cmd, shell = True)
        if do_shutdown == 1:
            cmd = "sudo shutdown now"
            subprocess.Popen(cmd, shell = True)
        time.sleep(1)

