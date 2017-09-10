import time
import logging
import serial

STARTBLOCK = "SB"
RECORD_LENGTH = "RL"
RECORD_CB = "CB"

# Ofsets of the PM data (always 2 byte)
BAUD_RATE = "baudrate"
BYTE_ORDER = "byte_order"
SUPPORTED_VALUES = "supported_values"


LOGGER = logging.getLogger(__name__)

class DataReader(object):
    def __init__(self, start_bytes, protocol_length, record_parse_cb, user_cb):
        self.start_bytes = start_bytes
        self.protocol_length = protocol_length
        self.buffer = bytearray()
        self.record_parse_cb = record_parse_cb
        self.user_cb = user_cb

    def process_data(self, data):
        self.buffer.extend(bytearray(data))
        while self.buffer:
            if len(self.buffer) < len(self.start_bytes):
                return
            if self.buffer[:len(self.start_bytes)] == self.start_bytes:
                # We have found the start bytes
                if len(self.buffer) < self.protocol_length:
                    return
                record = self.buffer[len(self.start_bytes):self.protocol_length]
                self.buffer = self.buffer[self.protocol_length:]
                self.user_cb(self.record_parse_cb(record))
            if self.buffer:
                self.buffer.pop(0)

def default_callback(data):
    """The default callback, print the data from the sensor"""
    LOGGER.warning("No Callback configured. Data is: %r", data)

class PySerialCollector(object):
    def __init__(self,
                 serialdevice,
                 configuration,
                 callback=default_callback,
                 scan_interval=0):
        self._run = True

        self.reader = DataReader(
            configuration[STARTBLOCK],
            configuration[RECORD_LENGTH],
            configuration[RECORD_CB],
            callback)

        self.scan_interval = scan_interval
        self.serial = serial.Serial(port=serialdevice,
                                    baudrate=configuration[BAUD_RATE],
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS)

    def stop(self):
        self._run = False

    def run(self):
        while self._run:
            if self.serial.in_waiting > 0:
                self.reader.process_data(self.serial.read(self.serial.in_waiting))
            else:
                time.sleep(.2)
