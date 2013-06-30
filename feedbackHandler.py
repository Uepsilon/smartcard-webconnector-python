import RPi.GPIO as GPIO

SUCCESS = 15
POWER = 13
ERROR = 11
CONNECTION = 16

ACTIVE = GPIO.HIGH
INACTIVE = GPIO.LOW

def setup():
    # Set GPIO-Mode to BCM
    GPIO.setmode(GPIO.BOARD)

    # Define GPIO-Output LEDs
    GPIO.setup(POWER, GPIO.OUT, initial=GPIO.HIGH) # Power-Indikator

    GPIO.setup(SUCCESS, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ERROR, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(CONNECTION, GPIO.OUT, initial=GPIO.LOW)

def setFeedback(channel, status):
    GPIO.output(channel, status);

def shutdown():
    # Turn all LEDs off before leaving
    GPIO.output(POWER, INACTIVE)
    GPIO.output(SUCCESS, INACTIVE)
    GPIO.output(ERROR, INACTIVE)
    GPIO.output(CONNECTION, INACTIVE)

    # and free GPIO-Interface
    GPIO.cleanup()

