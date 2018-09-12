import sys
import Adafruit_DHT
import time
import datetime
import RPi.GPIO as GPIO
import os
import csv

def check_path(filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.direname(filename))

        with open(filename, "a") as csv_file:
            data_writer = csv.write(csv_file, delimiter=',')
            data_writer.writerow(["Time", "Temperature", "Humidity"])

def write_to_csv(temperature, humidity):
    current_date_time = datetime.datetime.now()

    # Set file to current hour in directory of the date. Example: "2018/9/12/16.csv"
    filename = "/home/pi/RaspberryBeerFridge/logs/" + str(current_date_time.year) + "/" + str(current_date_time.month) + "/" + str(current_date_time.day) + "/" + str(current_date_time.hour) + ".csv"
    check_path(filename)

    with open(filename, "a") as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',')
        data_writer.writerow([str(current_date_time.time()), str(temperature), str(humidity)])

def write_to_txt(text):
    current_date_time = datetime.datetime.now()

    filename = "/home/pi/RaspberryBeerFridge/logs/" + str(current_date_time.year) + "/" + str(current_date_time.month) + "/" + str(current_date_time.day) + "/" + str(current_date_time.hour)
    check_path(filename)

    with open(filename, "a") as myfile:
        myfile.write(text)
        myfile.write('\n')

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

GPIO.setmode(GPIO.BCM)

SENSOR_TYPE = sensor_args['11']
SENSOR_PIN = 3
RELAIS_1_GPIO = 26
LED_1_GPIO = 21
MAX_TEMP = 6
MIN_TEMP = 5

fridge_state = "high"
last_time =  datetime.datetime.now() - datetime.timedelta(minutes=5)

GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
GPIO.setup(LED_1_GPIO, GPIO.OUT)

GPIO.output(LED_1_GPIO, GPIO.HIGH)
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).

write_to_txt("Starting up!")

while True:
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_PIN)
    if humidity is not None and temperature is not None:
        write_to_csv(temperature, humidity)

        if temperature > MAX_TEMP:
            diff = datetime.datetime.now() - last_time
            diff_seconds = diff.total_seconds()
            if  diff_seconds > 300:
                if fridge_state == "high":
                    last_time = datetime.datetime.now()
                    fridge_state = "low"
                    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
                    write_to_txt(str(datetime.datetime.now()) + " Turning the fridge on")

        elif temperature < MIN_TEMP:
            if fridge_state == "low":
                fridge_state = "high"
                GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
                write_to_txt(str(datetime.datetime.now()) + " Turning the fridge off")
    else:
        write_to_txt(str(datetime.datetime.now()) + " Failed to get reading. Try again!")
        sys.exit(1)
    time.sleep(5)
