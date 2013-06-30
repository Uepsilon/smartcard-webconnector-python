#! /usr/bin/env python
"""
Smartcard Webconnector - Idenify with your Smartcard!

Usage:
    webconnector.py -U=<url> -E=<event-key> [-d=<delay>]
    webconnector.py -h
    webconnector.py --version

Options:
    -U --url=<url>                      Url to POST to
    -E --event-key=<event-key>          Event-Key
    -d --delay=<delay>                  Delay between Connection-Checks              
    -h --help                           Shows this Screen
    --version                           Shows the Version
"""


import threading
import feedbackHandler
import time
import urllib2

from cardWebconnector import cardWebconnector
from smartcard.CardMonitoring import CardMonitor, CardObserver
from docopt import docopt

class Webconnector():

    cardmonitor = None
    cardobserver = None

    """
        MainClass for the Webconnector
    """
    def __init__(self, args):
        feedbackHandler.setup()

        self.cardmonitor = CardMonitor()
        self.cardobserver = cardWebconnector(args)

        self.addCardObserver(self.cardobserver)

    def shutdown(self):
        print "Shutdown"
        self.removeCardObserver(self.cardobserver)
        feedbackHandler.shutdown()

    def addCardObserver(self, observer):
        self.cardmonitor.addObserver(observer)

    def removeCardObserver(self, observer):
        self.cardmonitor.deleteObserver(observer)

    def checkConnection(self, url):
        try:
            # Try connection
            response = urllib2.urlopen(url, timeout=1)

            # Connection successful, activate Connection-LED
            feedbackHandler.setFeedback(feedbackHandler.CONNECTION, feedbackHandler.ACTIVE)

            return True
        except urllib2.URLError as e:
            # No Connection to Server
            feedbackHandler.setFeedback(feedbackHandler.CONNECTION, feedbackHandler.INACTIVE)
        finally:
            return False

if __name__ == '__main__':
    try:
        args = docopt(__doc__, version='Smartcard Webconnector: 0.1')

        if args['--delay'] is None:
            timeout = 10
        else:
            timeout = int(args['--delay'])

        webconnector = Webconnector(args)

        while True:
            # Wait for SIGTERM and check connection every now and then
            webconnector.checkConnection(args['--url'])
            time.sleep(timeout)
    finally:
        try:
            webconnector.shutdown()
        except NameError:
            # webconnector not defined, nothing to do here
            pass
