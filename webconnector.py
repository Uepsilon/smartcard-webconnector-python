#! /usr/bin/env python
"""
Smartcard Webconnector - Idenify with your Smartcard!

Usage:
    webconnector.py -U=<url> -E=<event-key>
    webconnector.py -h
    webconnector.py --version

Options:
    -U --url=<url>                      Url to POST to
    -E --event-key=<event-key>          Event-Key
    -h --help                           Shows this Screen
    --version                           Shows the Version
"""

from smartcard.CardMonitoring import CardMonitor, CardObserver
from docopt import docopt
# import RPi.GPIO as GPIO
import threading

from cardWebconnector import cardWebconnector

class Webconnector():
    indicatorLeds = {
        'success': 11,
        'error': 13,
        'connection': 15,
        'power': 16
    }

    cardmonitor = None
    cardobserver = None

    """
        MainClass for the Webconnector
    """
    def __init__(self, args):
        # Set GPIO-Mode to BCM
        # GPIO.setmode(GPIO.BOARD)

        # Define GPIO-Output LEDs
        # for led, port in indicatorLeds.iteritems():
        #     if led is 'power':
        #         GPIO.setup(port, GPIO.OUT, initial=GPIO.HIGH)
        #     else:
        #         GPIO.setup(port, GPIO.OUT, initial=GPIO.LOW)

        self.cardmonitor = CardMonitor()
        self.cardobserver = cardWebconnector(args)

        self.addCardObserver(self.cardobserver)

        while True:
            pass


            # self.switchLed(indicatorLeds['success'], GPIO.Low)
            # self.switchLed(indicatorLeds['error'], GPIO.Low)

    def shutdown(self):
        self.removeCardObserver(self.cardobserver)

    def addCardObserver(self, observer):
        self.cardmonitor.addObserver(observer)

    def removeCardObserver(self, observer):
        self.cardmonitor.deleteObserver(observer)

    def connectionAvailable(self, uid):
        try:
            # Try connection
            urllib2.urlopen(self.url, timeout=1)

            # Connection successful, activate Connection-LED
            # self.switchLed(self.indicatorLeds['connection'], GPIO.HIGH)
            return True
        except urllib2.URLError as e:
            print "No Connection to Server"
            # self.switchLed(self.indicatorLeds['connection'], GPIO.LOW)
        finally:
            return False

    # def switchLed(self, port, status):
        print str(port) + " will be set to " + str(status)
        # GPIO.output(port, status);


if __name__ == '__main__':
    try:
        args = docopt(__doc__, version='Smartcard Webconnector: 0.1')
        webconnector = Webconnector(args)
    finally:
        webconnector.shutdown()
        # GPIO.cleanup()
