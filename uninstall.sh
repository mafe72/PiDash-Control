#!/bin/bash

#Step 1) Check if root--------------------------------------
if [[ $EUID -ne 0 ]]; then
   echo "Please execute script as root." 
   exit 1
fi
#-----------------------------------------------------------

#Step 2) Remove Installation directory ---------------------

cd /opt/
sudo rm -r PiDashControl

#-----------------------------------------------------------

#Step 3) Remove configuration script ------------
cd /etc/
RC=rc.local

#Cleaning deprecated configration files --------------------
echo Removing configration files from rc.local

if grep -q "sudo python3 \/opt\/PiDashControl\/pidashctrl.py \&" "$RC";
        then
	sed -i '/sudo python3 \/opt\/PiDashControl\/pidashctrl.py \&/c\' "$RC";
fi

#-----------------------------------------------------------
#Step 4) Reboot to apply changes----------------------------
echo "PiDash Control un-install complete. Will now reboot after 3 seconds."
sleep 4
sudo reboot
#-----------------------------------------------------------
