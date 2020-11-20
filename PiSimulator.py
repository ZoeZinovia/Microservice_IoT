import pika
import os
import time
import json
from datetime import datetime

message_interval = 20
reading_interval = 5
sensor = 22
pin = 12

#Access the CLODUAMQP_URL environment variable
# url = os.environ.get("CLOUDAMQP_URL")
params = pika.URLParameters("amqps://evwdjvwe:Lo9EpIkj1Z0teejABG64oO8UIIOhxyU8@jaguar.rmq.cloudamqp.com/evwdjvwe")  #Pika is a pure-Python implementation of the AMQP 0-9-1 protocol that tries to stay fairly independent of the underlying network support library.
connection = pika.BlockingConnection(params)

#Start a channel
channel = connection.channel()

#Declare a queue
channel.queue_declare(queue="weather")

isSimulation = 0
if isSimulation:
	import random
	def genrand():
		return random.random(), random.random()*100 #Python library to read the DHT series of humidity and temperature sensors on a Raspberry Pi or Beaglebone Black
else:
	import Adafruit_DHT

while True:
	body = []
	timeout = time.time() + message_interval
	while True:
		if time.time() > timeout:
			break
		if isSimulation:
			humidity, temperature = genrand()
		else:
			humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		read_time = datetime.now()
		d = {"t": str(read_time), "T": temperature, "H": humidity}
		body.append(d)
		time.sleep(reading_interval)

		print("sending data")
		channel.basic_publish(exchange='', routing_key='weather', body = json.dumps(body))

connection.close()