# Smartcard Webconnector

A small interface to read and check a smartcard and use it as an Identification
in a Webservice

## Usage
python connector.py --url=URL (--resource=RESOURCE)  
python connector.py -U URL (-R RESOURCE)  
python connector.py --help  

* URL is the URL the Card-Id will be send to
* RESOURCE is used as an universal Parameter (e.g. to tell from which checkpoint
somone authenticates)

### Requirements
You'll need this stuff in order to be able to use this script.

Python:  
* [pyscard](http://pyscard.sourceforge.net/) -> Library for Python to use PC/SC
* docopt

Global:  
* [pcsc](http://en.wikipedia.org/wiki/PC/SC)
* A Cardreader (for obvious Reasons)
* A SmartCard (e.g. Mifare-Cards like Classic / Ultralight)

### Install (on clean Raspbian)

1. Install system dependencies
  ```
  sudo apt-get install dh-autoreconf libudev-dev flex
  sudo apt-get install pcscd libusb-dev libpcsclite1 libpcsclite-dev dh-autoreconf pcsc-tools
  sudo apt-get install swig python-dev
  ```

2. Install [pyscard](http://pyscard.sourceforge.net/)
   ```
   git clone https://github.com/LudovicRousseau/pyscard.git
   cd pyscard
   rm -rf build
   sudo rm -rf build
   sudo python setup.py build
   sudo python setup.py install
   ```

3. Install python dependencies
   ```
   pip install --user docopt
   ```
