import urllib
import urllib2
import sys
import json
import hashlib
from smartcard.util import *

# import RPi.GPIO as GPIO

# define the apdus used in this script
GET_RESPONSE = [0XA0, 0XC0, 0x00, 0x00]
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

class cardWebconnector(object):
    lastId = None
    url = None
    eventKey = None

    def __init__(self, args):
        self.url = args['--url']
        self.eventKey = args['--event-key']

        # Set GPIO-Mode to BCM
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

    def update(self, observable, (addedcards, removedcards)):
        for card in addedcards:
            # Create connection
            connection = card.createConnection()
            connection.connect()

            # Get Reader-ID as Resource
            resource = self.getReaderID(connection)

            # Get Card-UID
            cardUID = self.getUID(connection)
            print "Inserted Card with UID: " + str(cardUID)

            if self.checkNewUID(cardUID):
                # here we go
                self.webConnect(cardUID, resource)
            else:
                print "#### Same UID ( " + str(cardUID) + " ) as Before... Skipping... ####"

    def webConnect(self, uid, resource):
        request_data = {}
        request_data['card_uid'] = "".join(map(str, uid))
        request_data['event_key'] = self.eventKey
        request_data['resource'] = resource

        try:
            print "Calling " + str(self.url) + " with Options: " + str(request_data)
            request = urllib2.Request(self.url, data=json.dumps(request_data))
            request.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(request)

            if response.code is 200:
                self.processWebResponse(response)
                # Turn Success-LED on
                # GPIO.output(15, GPIO.HIGH)
            else:
                # Turn Error-LED on
                # GPIO.output(11, GPIO.HIGH)

                print "Error from Webservice: " + str(response.code)
        except urllib2.URLError as e:
            print "No Connection to Server"
            # self.switchLed(self.indicatorLeds['connection'], GPIO.LOW)
        except Exception as e:
            print e

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

    def processWebResponse(self, response):
        if 'application/json' in response.info().getheader('Content-Type') :
            print json.loads(response.read())
        else:
            print response.info().getheader('Content-Type')
