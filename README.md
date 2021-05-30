# PiDash-Control
This is a system info display with a button interface for soft-shutdown and reboot of the Raspberry Pi.

License
-------
<div align="center"><a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Attribution-NonCommercial-ShareAlike" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /></div>

This project is licensed under the Attribution-NonCommercial-ShareAlike CC BY-NC-SA 4.0 license. The full legal text of the license may be found in the LICENSE.md file in this repository. For more information about this license, please visit 
the Creative Commons Foundation (https://creativecommons.org/licenses/by-nc-sa/4.0/).

Features
--------


Hardware Installation
---------------------


Software Installation
---------------------

**NOTE**: This assumes that you have already connected the jumper wires to the correct PINS and ports;
If you haven't, see the [Hardware Installation](#hardware-installation) section.

This instructions are a *step-by-step guide* to install necessary software for the **PiDash-Control**.
You can setup this via SSH or using the command line interface in your RetroPie. To enter the command line interface of RetroPie, *PRESS* ***F4*** just after booting up.

----------

Open your terminal and type the one-line installation command below:
```bash
wget -O - "https://raw.githubusercontent.com/mafe72/PiDash-Control/master/install.sh" | sudo bash
```

The script will automatically install pertinent files and configure your Raspberry Pi to enable **PiDash-Control.**
Installation will automatically reboot once all processes is completed.

After rebooting, your **PiDash-Control** is now fully functional.

Software Uninstall
---------------------

This instructions are a *step-by-step guide* to uninstall necessary software for your **PiDash-Control**.
You can setup this via SSH or using the command line interface in your RetroPie. To enter the command line interface of RetroPie, *PRESS* ***F4*** just after booting up.

----------

Open your terminal and type the one-line installation command below:
```bash
wget -O - "https://raw.githubusercontent.com/mafe72/PiDash-Control/master/uninstall.sh" | sudo bash
```

The script will automatically uninstall all configuration files from your Raspberry Pi to disable the **PiDash-Control.**
The uninstall script will automatically reboot once all processes are completed.

After rebooting, your **PiDash-Control** will be fully deactivated.

----------

Basic Hardware Usage
--------------------


Basic Software Usage
--------------------


Basic Maintenance
-----------------

