#!/bin/bash

#Step 1) Check if root--------------------------------------
if [[ $EUID -ne 0 ]]; then
   echo "Please execute script as root." 
   exit 1
fi
#-----------------------------------------------------------
CNF=/boot/config.txt
RC=/etc/rc.local
DIR=/opt/PiDashControl
script=/opt/PiDashControl/pidashctrl.py
SourcePath=https://raw.githubusercontent.com/mafe72/PiDash-Control/master/scripts

#-----------------------------------------------------------
#Step 2) Enable required services and update repository-----

if grep -q "avoid_warnings=0" "$CNF";
        then
		sed -i '/avoid_warnings=0/d' "$CNF";
fi
if grep -q "avoid_warnings=1" "$CNF";
        then
                echo "warnings already disabled. Doing nothing."
        else
                echo "avoid_warnings=1" >> "$CNF"
                echo "warnings disable."
fi
# Enable I2C
if grep -q "#dtparam=i2c_arm=on" "$CNF";
        then
                sed -i '/dtparam=i2c_arm=on/d' "$CNF";
fi
if grep -q "dtparam=i2c_arm=on" "$CNF";
        then
                echo "I2C already enabled. Doing nothing."
        else
                echo "dtparam=i2c_arm=on" >> "$CNF"
                echo "I2C enabled."
fi
# Enable SPI
if grep -q "#dtparam=spi=on" "$CNF";
        then
                sed -i '/dtparam=spi=on/d' "$CNF";
fi
if grep -q "dtparam=spi=on" "$CNF";
        then
                echo "SPI already enabled. Doing nothing."
        else
                echo "dtparam=spi=on" >> "$CNF"
                echo "SPI enabled."
fi
# Update repository
sudo apt-get update -y
#-----------------------------------------------------------

#Step 3) Install required modules----------------------------
sudo apt-get install -y python3-pip python3-pip python3-gpiozero i2c-tools
sudo pip3 install psutil pyserial adafruit-circuitpython-ssd1306 --break-system-packages
#-----------------------------------------------------------

#Step 4) Download Python script-----------------------------
sudo mkdir $DIR

if [ -e $script ];
	then
		echo "Script already exists. Updating..."
		rm $script
		wget -O $script "$SourcePath/pidashctrl.py"
		echo "Update complete."
	else
		wget -O $script "$SourcePath/pidashctrl.py"
        	echo "Download  complete."
fi
#-----------------------------------------------------------

#Step 5) Enable Python script to run on start up------------
# Ensure /etc/rc.local exists with basic structure----------
if [ ! -f "$RC" ]; then
    echo "Creating /etc/rc.local..."
    {
        echo "#!/bin/sh -e"
        echo "#"
        echo "# rc.local"
	echo "#"
	echo "#"
 	echo ""
  	echo ""
        echo "exit 0"
    } > "$RC"
    chmod +x "$RC"
    echo "/etc/rc.local created with default content."
fi
# Adding new configuration----------- 
if grep -q "sudo python3 \/opt\/PiDashControl\/pidashctrl.py \&" "$RC";
	then
		echo "Auto start  already configured. Doing nothing."
	else
		sed -i -e "s/^exit 0/sudo python3 \/opt\/PiDashControl\/pidashctrl.py \&\n&/g" "$RC"
		echo "Auto start configured."
fi

#-----------------------------------------------------------

#Step 6) Reboot to apply changes----------------------------
echo "PiDash Control installation completed. Rebooting after 3 seconds."
sleep 4
sudo reboot
#-----------------------------------------------------------
