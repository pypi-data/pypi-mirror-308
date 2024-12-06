"""
    This file is part of GSOF_ArduBridge.

    GSOF_ArduBridge is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GSOF_ArduBridge is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GSOF_ArduBridge.  If not, see <https://www.gnu.org/licenses/>.

Class to communicate with an Arduino board running the GSOF-Ardubridge firmware.
The class creats an instance of BridgeSerial.ArduBridgeComm and saves it as self.comm.
It also creates instances of several other classes: ArduGPIO.ArduBridgeGPIO, ArduAnalog.ArduBridgeAn,
ArduI2C.ArduBridgeI2C, ArduSPI.ArduBridgeSPI, and CAP.ArduBridgePnS. These classes provide methods for
interacting with the Arduino's analog inputs, digital inputs and outputs, I2C bus, SPI bus, and pulse and
sample functionality, respectively.

"""

__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = "Copyright 2019"
__credits__ = ["James Perry"]
__license__ = "GPL-3.0-or-later"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Production"

import sys, time
import serial.tools.list_ports as listPorts
import logging
from GSOF_ArduBridge import BridgeSerial
from GSOF_ArduBridge import ArduAnalog
from GSOF_ArduBridge import ArduGPIO
from GSOF_ArduBridge import ArduI2C
from GSOF_ArduBridge import ArduSPI
from GSOF_ArduBridge import ArduPulseAndSample as CAP
from GSOF_ArduBridge import ArduWs2812

def findArduCom(lookFor="Arduino"):
    ports = listPorts.comports()
    for port in ports:
        if lookFor in port.description:
            return port.device
    return None

class ArduBridge():
    def __init__(self, COM="auto", baud=115200*2, logger=None, logLevel=logging.INFO, fileHandler=False, consoleHandler=True, RxTimeOut=0.015):

        version = 'v1.1 running on Python %s'%(sys.version[0:5])
        self.logger = logger
        if self.logger == None:
            self.logger = self._initLogger(logLevel=logLevel, fileHandler=fileHandler, consoleHandler=consoleHandler)
        self.logger.info('GSOF_ArduBridge %s'%(version))
        self.ExtGpio = [0,0]
        self.COM = COM
        if self.COM == "auto":
            self.COM = findArduCom(lookFor="Arduino")
            if self.COM == None:
                raise Exception("Couldn't find arduio, try to manualy specify its port.")
            else:
                if self.logger != None:
                    self.logger.info(f"Arduino on port '{self.COM}' is being used.")

        self.comm = BridgeSerial.ArduBridgeComm( COM=self.COM, baud=baud, logger=self.logger, RxTimeOut=RxTimeOut )
        self.gpio = ArduGPIO.ArduBridgeGPIO( bridge=self.comm, logger=self.logger )
        self.an   = ArduAnalog.ArduBridgeAn(bridge=self.comm, logger=self.logger )
        self.i2c  = ArduI2C.ArduBridgeI2C( bridge=self.comm, logger=self.logger)
        self.spi  = ArduSPI.ArduBridgeSPI( bridge=self.comm, logger=self.logger)
        self.cap  = CAP.ArduBridgePnS( bridge=self.comm, logger=self.logger)
        self.ws   = ArduWs2812.ArduBridgeWs2812( bridge=self.comm, logger=self.logger)     
    
    def _initLogger(self, logLevel=logging.INFO, fileHandler=True, consoleHandler=True):
        """Initialize the logger with a console handler and an optional file handler"""
        logger = logging.getLogger('GSOF_ArduBridge')
        logger.setLevel(logLevel)
        if consoleHandler:
            ch = logging.StreamHandler()
            ch.setLevel(logLevel)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        if fileHandler:
            fh = logging.FileHandler('GSOF_ArduBridge.log')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        return logger

    def OpenClosePort(self, val, retry=6):
        """
        Open (1, retry=6) or close (0) the serial port connection to the Arduino.
        retry = -1 will try to open the port indefinitely attempts.
        """
        if type(val) == str:
            if val == 'open':
                val = 1
            else:
                val = 0
        self.comm.OpenClosePort(val)
        if val != 0:
            while (self.GetID() == False) and (retry != 0):
                self.logger.debug("Open port retry# {retry}")
                time.sleep(0.5)
                if retry > 0:
                    retry -= 1
            arduRespond = self.GetID()
            if arduRespond == False:
                self.logger.critical(f"Failed to connect to arduBridge on device {self.COM}")
            else:
                self.logger.info(f"Connected to arduBride with response {arduRespond}")
        return retry

    def Reset(self):
        """Sends a reset command to the Arduino and flushes the serial buffer"""
        self.comm.sendReset()
        self.comm.uart_flush()
        self.GetID()

    def GetID(self):
        """Sends a request for ID and returns the the reply if received, or False otherwise"""
        self.comm.send([ord('?')])
        reply = self.comm.receive(1)
        if reply[0] > 0:
            s = ''
            ACK = 1
            N = reply[1][0]
            while (ACK > 0) and (N > 0):
                reply = self.comm.receive(1)
                ACK = reply[0]
                if ACK > 0:
                    N -= 1
                    s += chr(reply[1][0])
            s += '\n'
            print('%s'%(s))
            if reply[0] == 1:
                #print('Got reply\n')
                return s
            return False
        else:
            print('No reply')
            return False
