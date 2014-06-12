from app import flapp, socketio
from threading import Thread

import os
import shutil
from random import sample, gauss
import time
import argparse
from app import rcon
from random import sample
import serial
import re



def read_serial_port():
	
	device = '/dev/' + filter(lambda x: re.match('tty.usbmodem*', x), os.listdir('/dev'))[0]
	serial_connection = serial.Serial(device, 9600)
	
	while True:
		reading = serial_connection.readline()
		reading = int((int(reading) / 1024.0) * 255)
		rgb = (reading, 128, 64)
		color = '#'+''.join(map(chr, rgb)).encode('hex')
		print 'From serial:', color
		socketio.emit('new serial data', {'color':color}, namespace = '/serial')
		# time.sleep(0.1)

if __name__ == "__main__":
	Thread(target = read_serial_port).start()
	socketio.run(flapp, port = 8080)
