#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import board
import paho.mqtt.client as mqtt
import signal
import sys
import random
import adafruit_ahtx0

brokerHost = "10.30.50.201"
siteId = "laboIoT"

i2c = board.I2C()  # uses board.SCL and board.SDA
temperatureSensor = adafruit_ahtx0.AHTx0(i2c)

def senData(sensorId=None, measurement=None, value=None):
    mqttc.publish("sensors/{}/{}/{}".format(siteId, sensorId, measurement),value, qos=2)

#------------------------------
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

# Fonction permettant d'initialiser les pins / capteurs / callbacks events / ...
def setupGPIO():
    GPIO.setmode(GPIO.BCM)#met en en mode BCM => GPIO17 = 17
    signal.signal(signal.SIGINT, signal_handler)#afin de bien quitter le programme lors de ctr+c
 
#-----MQTT Client init------
mqttc = mqtt.Client()
# mqttc.username_pw_set(user_broker, password_broker)# USER AND PASSWORD
mqttc.connect(brokerHost, 31111, 60)
mqttc.loop_start() # The loop automatically reconnect in cas of disconnections


if __name__ == '__main__':
    setupGPIO()
    current_time = time.time()
    previous_time = current_time
    sendDataDelay = 60 # seconds
    temp = 0
    while True:
        current_time = time.time()
        temp = temperatureSensor.temperature
        humidity = temperatureSensor.relative_humidity

        if(current_time - previous_time > sendDataDelay): 
            senData(sensorId="labo_humidity_1", measurement="humidity", value=temp)
            previous_time = time.time()
        
        time.sleep(.2)