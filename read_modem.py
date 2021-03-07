#!/usr/bin/env python3.7

import serial
import glob
import re
import time
import sys

usb=sys.argv[1]
imei=sys.argv[2]

try:
	ser = serial.Serial(usb, 19200, timeout=1)
	#ser.write(b'AT+CPMS="MT"\r\n') # Nastaveni storage SIM + Modem
	#ser.write(b'AT+CMGF=1\r\n') # SMS textovy mod
	ser.write(b'AT+CMGL="ALL"\r\n') # List zprav (vsech)
	#ser.write(b'AT+CMGR=1\r\n') # Cteni zpravy (ID=1) cisluje se od 0
	#ser.write(b'AT+CMGD=0\r\n') # Mazani zpravy (ID=1) cisluje se od 0
	line = ser.read(20000)
	print(line.decode("utf-8"))
	ser.close()
except:
	print("Can't open %s." % (usb))
