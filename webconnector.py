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

from smartcard.util import *
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from docopt import docopt
import RPi.GPIO as GPIO
import urllib2
import sys
import json
import hashlib
import threading

# define the apdus used in this script
GET_RESPONSE = [0XA0, 0XC0, 0x00, 0x00]
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]


class Webconnector():
    cardType = ATRCardType(
        toBytes("3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 01 00 00 00 00 6A"),  # Card Type
        toBytes("FF FF FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00")   # Card Mask
    )
    cardRequest = None
    lastId = None
    url = None
    resource = None
    eventKey = None

    indicatorLeds = {
        'success': 11,
        'error': 13,
        'connection': 15,
        'power': 16
    }

    """
        MainClass for the Webconnector
    """
    def __init__(self, args):
        # set url + Resource
        self.url = args['--url']
        self.eventKey = args['--event-key']

        # Set GPIO-Mode to BCM
        GPIO.setmode(GPIO.BOARD)
     
        # Define GPIO-Output LEDs
        for led, port in indicatorLeds.iteritems():
            if led is 'power':
                GPIO.setup(port, GPIO.OUT, initial=GPIO.HIGH)
            else:
                GPIO.setup(port, GPIO.OUT, initial=GPIO.LOW)

        self.cardRequest = CardRequest(timeout=None, cardType=self.cardType)
        while True:
            cardservice = self.cardRequest.waitforcard()

            # At this point, a card is inserted -> Connect to that very card
            cardservice.connection.connect()

            # Get Reader-ID as Resource
            self.resource = self.getReaderID(cardservice.connection)

            cardUID = self.getUID(cardservice.connection)

            if self.checkNewUID(cardUID):
                # here we go
                print "UID: " + str(cardUID)
                self.webConnect(cardUID)
            else:
                print "#### Same UID ( " + str(cardUID) + " ) as Before... Skipping... ####"

            cardservice.connection.disconnect()

            # Ugly shit to check if the card has been removed
            while self.cardRequest.waitforcardevent():
                pass

    def webConnect(self, uid):
        request_data = {}
        request_data['card_uid'] = "".join(map(str, uid))
        request_data['event_key'] = self.eventKey

        if self.resource is not None:
            request_data['resource'] = self.resource

        try:
            print "Calling " + str(self.url) + " with Options: " + str(request_data)
            response = urllib2.urlopen(self.url, data=urllib2.urlencode(request_data))

            if response.code is 200:
                self.processWebResponse(response)
                # Turn Success-LED on for 2 Sec
                self.timedLedSwitch(indicatorLeds['success'], GPIO.HIGH, GPIO.LOW, 2)
            else:
                # Turn Error-LED on for 2 Sec
                self.timedLedSwitch(indicatorLeds['error'], GPIO.HIGH, GPIO.LOW, 2)
                
                print "Error from Webservice: " + str(response.code)
        except Exception as e:
            print e

    def checkConnection(self, uid):
        try:
            # Try connection
            urllib2.urlopen(self.url, timeout=1)

            # Connection successful, activate Connection-LED
            self.switchLed(self.indicatorLeds['connection'], GPIO.HIGH)
        except urllib2.URLError as e:
            self.switchLed(self.indicatorLeds['connection'], GPIO.LOW)


    def processWebResponse(self, response):
        if 'application/json' in response.info().getheader('Content-Type') :
            print json.loads(response.read())
        else:
            print response.info().getheader('Content-Type')

    def checkNewUID(self, uid):
        if uid == self.lastId or uid is False:
            return False
        else:
            self.lastId = uid
            return True

    def getReaderID(self, connection):
        # Read SHA1-Hash of Reader-Name (as Readers are addressed by Names not IDs)
        m = hashlib.sha1()
        m.update(str(connection.getReader()))
        return m.hexdigest()

    def getUID(self, connection):
        # Read UID from Card
        return self.executeCardCmd(connection, GET_UID)

    def executeCardCmd(self, connection, cmd):
        response, sw1, sw2 = connection.transmit(cmd)
        if not self.validateCardResponse(sw1, sw2):
            print "CMD: " + str(cmd)
            sys.exit(1)
        else:
            return response

    def validateCardResponse(self, sw1, sw2):
        response = False
        if sw1 is 0x90 and sw2 is 0x00:
            response = True
        elif sw1 is 0x67 and sw2 is 0x00:
            print "Wrong length (Lc incoherent with Data In)"
        elif sw1 is 0x68 and sw2 is 0x00:
            print "CLA byte is not correct"
        elif sw1 is 0x6a and sw2 is 0x81:
            print "Function not supported (INS byte is not correct), or not available for the selected card"
        elif sw1 is 0x6B and sw2 is 0x00:
            print "Wrong parameter P1-P2"
        elif sw1 is 0x6F and sw2 is 0x01:
            print "Card mute (or removed)"
        return response

    def switchLed(self, port, status):
        print str(port) + " will be set to " + str(status)
        GPIO.output(port, status);

    def timedLedSwitch(self, port, init, end, time):
        # set init value
        self.switchLed(port, init)

        # create and start Timer to Call switchLed again after given Time
        thread = threading.Timer(time, switchLed, [port, end]).start()



if __name__ == '__main__':
    try: 
        args = docopt(__doc__, version='Smartcard Webconnector: 0.1')
        webconnector = Webconnector(args)
    finally:
        GPIO.cleanup()
