import serial
import urllib2
import os
import re
import numpy
import time
from Queue import Queue, Empty
from threading import Thread, Event
from logging import Logger, FileHandler
logger = Logger(__name__)
logger.addHandler(FileHandler('log.txt'))
logger.setLevel('DEBUG')


# url = "http://cryptic-harbor-7040.herokuapp.com:8080/color"
url = "http://107.170.251.142:8080/color"
# url = "http://127.0.0.1:8080/color"



queue = Queue()

def read_serial(name, is_running):
	logger.debug('Running %s'%name)
	device = '/dev/' + filter(lambda x: re.match('tty.usbmodem*', x), os.listdir('/dev'))[0]

	logger.debug('Opening device %s'%device)
	serial_connection = serial.Serial(device, 9600)

	values = list()
	previous_reading = 0

	while is_running.isSet():
		reading = serial_connection.readline()
		reading = int((int(reading) / 1024.0) * 255)
		
		if reading != previous_reading:
			queue.put(reading)
			previous_reading = reading
		
		logger.debug('reading: %s'%reading)
		time.sleep(0.1)
	
	serial_connection.close()


def send_data(name, is_running):
	logger.debug('Running %s'%name)
	while is_running.isSet():
		try:
			red = queue.get(timeout = 0.001)
			
			rgb = (red, 100, 100)
			color = '#'+''.join(map(chr, rgb)).encode('hex')
			logger.debug('Sending HTTP request with color: %s'%color)

			request = urllib2.Request('http://107.170.251.142/color', data = color, headers = {'Content-Type':'text/plain'})
			response = urllib2.urlopen(request)
		except Empty:
			pass

if __name__ == "__main__":
	logger.info('*******************************************************\n')
	logger.info('Process id: %s', os.getpid())
	



	is_running = Event()
	is_running.set()

	
	serial_reader = Thread(target = read_serial, args = ('Serial reader', is_running))
	serial_reader.start()

	
	data_sender = Thread(target = send_data, args = ('Data sender', is_running))
	data_sender.start()
	
	try:
		while True:
			time.sleep(0.1)
	except KeyboardInterrupt:
		is_running.clear()
		serial_reader.join()
		data_sender.join()
		# serial_connection.close()

	


	
		
		# request = urllib2.Request(url, color, {'Content-Type': 'text/plain'})
		# response = urllib2.urlopen(request)
		# print response
		# socketio.emit('new serial data', {'color':color}, namespace = '/serial')
		# time.sleep(0.1)
