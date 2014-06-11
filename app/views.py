from app import flapp, socketio
from flask import render_template

@flapp.route('/')
def static_wall():
	return render_template('index.html')


@socketio.on('request serial data', namespace = '/serial')
def send_images():
	flapp.logger.debug('Got images request in namespace: grid')
