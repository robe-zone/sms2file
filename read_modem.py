#!/usr/bin/env python3.7

import serial
import glob
import re
import time
import sys

usb=sys.argv[1]
imei=sys.argv[2]

# Omezeni:
#  - co zprava to file, neresim multipart SMS
#  - zpravy beru postupne, neresim jejich casovou posloupnost v ramci modemu

def send_command(ser, cmd):
	ser.write(bytes(cmd+'\r\n', "utf-8"))
	output = ser.read(20000)
	return output.decode("utf-8")

try:
	ser = serial.Serial(usb, 19200, timeout=1)
	# Nastaveni storage SIM + Modem
	send_command(ser, 'AT+CPMS="MT"')
	
	# SMS 1 - textovy mod 0 - PDU mode
	send_command(ser, 'AT+CMGF=0') 

	while ser.is_open:
		# Process messages in PDU
		# source: https://www.diafaan.com/sms-tutorials/gsm-modem-tutorial/at-cmgl-text-mode/
		msg_ids=send_command(ser, 'AT+CMGL=4')
		sms_regex = re.compile(r'\+CMGL: (\d+)')
		messages = sms_regex.findall(msg_ids)
		for msg in messages:
			print(send_command(ser, 'AT+CMGR='+msg))
			# How to read PDU / convert algorithm
			# source: https://www.diafaan.com/sms-tutorials/gsm-modem-tutorial/online-sms-deliver-pdu-decoder/
			# source: https://stackoverflow.com/a/19531128
			##### NEXT to continue
			exit()
		ser.close()

	#ser.write(b'AT+CMGR=1\r\n') # Cteni zpravy (ID=1) cisluje se od 0
	#ser.write(b'AT+CMGD=0\r\n') # Mazani zpravy (ID=1) cisluje se od 0

except:
	print("Can't open %s." % (usb))
