import serial
import urllib2
import os
import re
import numpy
import time
import sys
from Queue import Queue, Empty, Full
from threading import Thread, Event
from logging import Logger, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser

logger = Logger(__name__)
logger.setLevel('DEBUG')
filehandler = RotatingFileHandler('log.txt', maxBytes = 10**6)
streamhandler = StreamHandler(sys.stdout)
formatter = Formatter('%(asctime)s - %(thread)d - %(levelname)s - %(message)s')
filehandler.setFormatter(formatter)
streamhandler.setFormatter(formatter)
logger.addHandler(filehandler)
logger.addHandler(streamhandler)

parser = ArgumentParser()
parser.add_argument('-r', '--remote-host', help = 'Server IP address e.g., 107.170.251.142')
args = parser.parse_args()



queue = Queue(1)

def read_serial(name, is_running):
	logger.debug('Running %s'%name)
	device = '/dev/' + filter(lambda x: re.match('tty.usbmodem*', x), os.listdir('/dev'))[0]

	logger.debug('Opening device %s'%device)
	serial_connection = serial.Serial(device, 9600)

	values = list()
	previous_reading = 0

	while is_running.isSet():
		reading = serial_connection.readline()
		try:
			reading = int((int(reading) / 1024.0) * 255)
		except ValueError:
			print 'Problem reading serial port. Please try to run the program again!'	
			os._exit(1)

		if reading != previous_reading:
			try:
				queue.put_nowait(reading)
			except Full:
				logger.debug('Full queue. Discarding reding: %s'%reading)
			previous_reading = reading
		
		logger.debug('reading: %s'%reading)
		time.sleep(0.1)
	
	serial_connection.close()


def send_color(name, is_running):
	logger.debug('Running %s'%name)
	while is_running.isSet():
		try:
			latest_reading = queue.get(timeout = 0.1)
			
			rgb = (latest_reading, 100, 100)
			color = '#'+''.join(map(chr, rgb)).encode('hex')
			
			logger.info('Sending HTTP request with color: %s'%color)

			request = urllib2.Request(url, data = color, headers = {'Content-Type':'text/plain'})
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
	print args.remote_host

	if args.remote_host:
		url = "http://%s/color"%args.remote_host
		data_sender = Thread(target = send_color, args = ('Data sender', is_running))
		data_sender.start()
	else:
		print 'ATTENTION: Running without remote host, so no data is being sent to server'
	
	try:
		while True:
			time.sleep(0.1)
	except KeyboardInterrupt:
		is_running.clear()
		serial_reader.join()
		# data_sender.join()
