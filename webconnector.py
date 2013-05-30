
#! /usr/bin/env python

"""
Smartcard Webconnector - Idenify with your Smartcard!

Usage:
    webconnector.py -U=<url> -R=<resource> -E=<event>
    webconnector.py -h
    webconnector.py --version

Options:
    -U --url=<url>              Url to POST to
    -R --resource=<resource>    Resource-Name
    -E --event=<event>          Event-ID
    -h --help                   Shows this Screen
    --version                   Shows the Version
"""

from smartcard.util import *
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from docopt import docopt
import urllib
import sys

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

    """
        MainClass for the Webconnector
    """
    def __init__(self, args):
        # set url + Resource
        self.url = args['--url']
        self.resource = args['--resource'] if args['--resource'] else None

        self.cardRequest = CardRequest(timeout=None, cardType=self.cardType)
        while True:
            cardservice = self.cardRequest.waitforcard()

            # At this point, a card is inserted -> Connect to that very card
            cardservice.connection.connect()

            cardUID = self.getUID(cardservice.connection)

            if self.checkNewUID(cardUID):
                # here we go
                self.webConnect(cardUID)
            else:
                print "Same UID as Before... Skipping..."

            cardservice.connection.disconnect()

            # Ugly shit to check if the card has been removed
            while self.cardRequest.waitforcardevent():
                pass

    def webConnect(self, uid):
        request_data = {}
        request_data['card_uid'] = "".join(map(str, uid))

        if self.resource is not None:
            request_data['resource'] = self.resource

        result = urllib.urlopen(self.url, data=urllib.urlencode(request_data))

        if result.code is 200:
            return True
        else:
            return False

    def checkNewUID(self, uid):
        if uid == self.lastId or uid is False:
            return False
        else:
            self.lastId = uid
            return True

    def getUID(self, connection):
        # Read UID from Card
        return self.transmission(connection, GET_UID)

    def transmission(self, connection, cmd):
        response, sw1, sw2 = connection.transmit(cmd)
        if not self.processResponse(sw1, sw2):
            print "CMD: " + str(cmd)
            sys.exit(1)
        else:
            return response

    def processResponse(self, sw1, sw2):
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


if __name__ == '__main__':
    webconnector = None

    args = docopt(__doc__, version='Smartcard Webconnector: 0.1')
    webconnector = Webconnector(args)
