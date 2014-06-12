import serial
import urllib2
import os
import re

url = "http://cryptic-harbor-7040.herokuapp.com/color"
url = "http://127.0.0.1:8080/color"
if __name__ == "__main__":
	device = '/dev/' + filter(lambda x: re.match('tty.usbmodem*', x), os.listdir('/dev'))[0]
	serial_connection = serial.Serial(device, 9600)
	


	while True:
		reading = serial_connection.readline()
		reading = int((int(reading) / 1024.0) * 255)
		rgb = (reading, 128, 64)
		color = '#'+''.join(map(chr, rgb)).encode('hex')
		print 'From serial:', color
		request = urllib2.Request(url, color, {'Content-Type': 'text/plain'})
		response = urllib2.urlopen(request)
		print response
		# socketio.emit('new serial data', {'color':color}, namespace = '/serial')
		# time.sleep(0.1)
