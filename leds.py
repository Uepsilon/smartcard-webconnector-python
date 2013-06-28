# import RPi.GPIO

class ledSignal(object):
    @staticmethod
    def setup():
        # Set GPIO-Mode to BCM
        # GPIO.setmode(GPIO.BOARD)

        # Define GPIO-Output LEDs
        # GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH) # Power-Indikator

        # GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
        pass

    @staticmethod
    def switchLed(port, status):
        print "#" + str(port) + ": " + str(status)
        # GPIO.output(port, status);

    @staticmethod
    def shutdown():
        # GPIO.cleanup()
        pass
