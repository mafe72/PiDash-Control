#!/bin/bash

#Step 1) Check if root--------------------------------------
if [[ $EUID -ne 0 ]]; then
   echo "Please execute script as root." 
   exit 1
fi
#-----------------------------------------------------------

#Step 2) Enable required services and Update repository----------------------------------
cd /boot/
File=config.txt
if grep -q "avoid_warnings=0" "$File";
        then
		sed -i '/avoid_warnings=0/d' "$File";
fi
if grep -q "avoid_warnings=1" "$File";
        then
                echo "warnings already disable. Doing nothing."
        else
                echo "avoid_warnings=1" >> "$File"
                echo "warnings disable."
fi
# Enable SPI
if grep -q "dtparam=spi=off" "$File";
        then
		sed -i '/dtparam=spi=o/d' "$File";
fi
if grep -q "dtparam=spi=on" "$File";
        then
                echo "SPI already enabled. Doing nothing."
        else
                echo "dtparam=spi=on" >> "$File"
                echo "SPI enabled."
fi
# Enable I2C
if grep -q "dtparam=i2c_arm=off" "$File";
        then
		sed -i '/dtparam=i2c_arm=on/d' "$File";
fi
if grep -q "dtparam=i2c_arm=on" "$File";
        then
                echo "I2C already enabled. Doing nothing."
        else
                echo "dtparam=i2c_arm=on" >> "$File"
                echo "I2C enabled."
fi
# Update repository
sudo apt-get update -y
#-----------------------------------------------------------

#Step 3) Install required modules----------------------------
sudo apt-get install -y python3-pip python3-pil python-smbus python-gpiozero i2c-tools
sudo pip3 install psutil pyserial adafruit-circuitpython-ssd1306
#-----------------------------------------------------------

#Step 4) Download Python script-----------------------------
cd /opt/
sudo mkdir PiDashControl
cd /opt/PiDashControl
script=pidashctrl.py

if [ -e $script ];
	then
		echo "Script pidash_ctrl.py already exists. Updating..."
		rm $script
		wget "https://raw.githubusercontent.com/mafe72/PiDash-Control/master/scripts/pidashctrl.py"
		echo "Update complete."
	else
		wget "https://raw.githubusercontent.com/mafe72/PiDash-Control/master/scripts/pidashctrl.py"
        echo "Download  complete."
fi
#-----------------------------------------------------------

#Step 5) Enable Python script to run on start up------------
cd /etc/
RC=rc.local

#Adding new configuration----------- 
if grep -q "sudo python3 \/opt\/PiDashControl\/pidashctrl.py \&" "$RC";
	then
		echo "File /etc/rc.local already configured. Doing nothing."
	else
		sed -i -e "s/^exit 0/sudo python3 \/opt\/PiDashControl\/pidashctrl.py \&\n&/g" "$RC"
		echo "File /etc/rc.local configured."
fi
#-----------------------------------------------------------

#Step 6) Reboot to apply changes----------------------------
echo "PiDash Control installation done. Will now reboot after 3 seconds."
sleep 4
sudo reboot
#-----------------------------------------------------------
