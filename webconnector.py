
#! /usr/bin/env python

"""
Smartcard Webconnector - Idenify with your Smartcard!

Usage:
    webconnector.py -U=<url> [-R=<resource>]
    webconnector.py -h
    webconnector.py --version

Options:
    -U --url=<url>              Url to POST to
    -R --resource=<resource>    Resource-Name to Identify on Webservice-Side
    -h --help                   Shows this Screen
    --version                   Shows the Version
"""

from smartcard.util import *
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from docopt import docopt
import urllib

# define the apdus used in this script
GET_RESPONSE = [0XA0, 0XC0, 00, 00]
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
                print self.webConnect(cardUID)
            else:
                print "Same UID as Before... Skipping..."

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
        response, sw1, sw2 = connection.transmit(GET_UID)

        if sw1 is 0x90:
            return response
        else:
            return False


if __name__ == '__main__':
    webconnector = None

    args = docopt(__doc__, version='Smartcard Webconnector: 0.1')
    webconnector = Webconnector(args)
