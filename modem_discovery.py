#!/usr/bin/env python3.7

import serial
import glob
import re
import subprocess
import os, signal
from os import path
import time

# Check PID
# source: https://stackoverflow.com/a/20186516
def pid_exists(pid): 
    if pid < 0: return False #NOTE: pid == 0 returns True
    try:
        os.kill(pid, 0) 
    except ProcessLookupError: # errno.ESRCH
        return False # No such process
    except PermissionError: # errno.EPERM
        return True # Operation not permitted (i.e., process exists)
    else:
        return True # no error, we can send a signal to the process

ttyUSB=glob.glob('/dev/ttyUSB*')
for usb in ttyUSB:
	try:
		tty=usb.split('/',2)[2]
		if path.exists("./lock/LCK.."+tty):
			f = open("./lock/LCK.."+tty, "r")
			lckPid = int(f.read())
			f.close()
			if pid_exists(lckPid):
				continue
		# source: https://pyserial.readthedocs.io/en/latest/
		ser = serial.Serial(usb, 19200, timeout=1)
		print("Opening %s" % (ser.name))
		ser.write(b'AT+GSN\r\n')
		line = ser.read(1000)
		imeiRegex = re.compile(r'(\d{15})')
		imei = imeiRegex.search(line.decode("utf-8"))
		print(imei.group())
		ser.close()
		p = subprocess.Popen(['/root/sms2file/read_modem.py', ser.name, imei.group()])
		f = open("./lock/LCK.."+tty, "w")
		f.write("%d" % p.pid)
		f.close()
	except:
		print("Can't open %s." % (usb))

print("waiting ...")

exit()
