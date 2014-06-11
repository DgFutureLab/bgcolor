from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from threading import Thread
import serial
import time
import os 
import re
flapp = Flask(__name__)

socketio = SocketIO(flapp)

# socketio.run(flapp, port = 5000)


def read_serial_port():
	device = '/dev/' + filter(lambda x: re.match('tty.usbmodem*', x), os.listdir('/dev'))[0]
	serial_connection = serial.Serial(device, 9600)
	
	while True:
		reading = serial_connection.readline();
		# print reading
		socketio.emit('new serial data', {'reading':reading}, namespace = '/')
		time.sleep(0.1)


@flapp.route('/')
def index():
	return render_template('index.html')


@socketio.on('request serial data', namespace = '/')
def send_images():
	print 'ASDLKJASDLKJASLKASJDLKAJSDLKJASD'
	# flapp.logger.debug('Got images request in namespace: grid')
	

if __name__ == "__main__":
	
		# time.sleep(100)	
	Thread(target = read_serial_port).start()
	socketio.run(flapp, port = 5000)
	# flapp.run(debug = True)