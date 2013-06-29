# import RPi.GPIO

# SUCCESS = 11
# POWER = 13
# ERROR = 15
# CONNECTION = 16

# ACTIVE = GPIO.HIGH
# INACTIVE = GPIO.LOW

SUCCESS = "Success"
POWER = "Power"
ERROR = "Error"
CONNECTION = "Connection"

ACTIVE = "Active"
INACTIVE = "Inactive"

def setup():
    # Set GPIO-Mode to BCM
    # GPIO.setmode(GPIO.BOARD)

    # Define GPIO-Output LEDs
    # GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH) # Power-Indikator

    # GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
    # GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
    # GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
    setFeedback(POWER, ACTIVE)

def setFeedback(channel, status):
    print "Set Channel '" + str(channel) + "' to '" + str(status) + "'"
    # GPIO.output(channel, status);

def shutdown():
    # GPIO.cleanup()
    pass
