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

import threading
from smartcard.CardMonitoring import CardMonitor, CardObserver
from docopt import docopt
from leds import ledSignal

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
        ledSignal.setup()

        self.cardmonitor = CardMonitor()
        self.cardobserver = cardWebconnector(args)

        self.addCardObserver(self.cardobserver)

        while True:
            pass

    def shutdown(self):
        self.removeCardObserver(self.cardobserver)
        ledSignal.shutdown()

    def addCardObserver(self, observer):
        self.cardmonitor.addObserver(observer)

    def removeCardObserver(self, observer):
        self.cardmonitor.deleteObserver(observer)

    def connectionAvailable(self, uid):
        try:
            # Try connection
            urllib2.urlopen(self.url, timeout=1)

            # Connection successful, activate Connection-LED
            ledSignal.switchLed(16, True)
            return True
        except urllib2.URLError as e:
            # No Connection to Server
            print "No Connection to Server"
            ledSignal.switchLed(16, False)
        finally:
            return False


if __name__ == '__main__':
    try:
        args = docopt(__doc__, version='Smartcard Webconnector: 0.1')
        webconnector = Webconnector(args)
    finally:
        webconnector.shutdown()
