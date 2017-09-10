from .serial_collector import (STARTBLOCK, RECORD_LENGTH, RECORD_CB,
                               BAUD_RATE, SUPPORTED_VALUES)

PM_1_0 = 'PM 1.0'
PM_2_5 = 'PM 2.5'
PM_10 = 'PM 10'
PM_ATM_1_0 = 'PM (atm) 1.0'
PM_ATM_2_5 = 'PM (atm) 2.5'
PM_ATM_10 = 'PM (atm) 10'
DB_0_3 = 'DB 0.3'
DB_0_5 = 'DB 0.5'
DB_1_0 = 'DB 1.0'
DB_2_5 = 'DB 2.5'
DB_5_0 = 'DB 5.0'
DB_10_0 = 'DB 10.0'
PM_10 = 'PM 10'

def sum_bytes(b1, b2):
    return (b1<<8) + b2

def parse_plantower(data):
    """
    PMS1003, PMS5003, PMS7003:
      32 byte long messages via UART 9600 8N1 (3.3V TTL).
    DATA(MSB,LSB): Message header (4 bytes), 2 pairs of bytes (MSB,LSB)
      -1(  1,  2): Begin message       (hex:424D, ASCII 'BM')
       0(  3,  4): Message body length (hex:001C, decimal 28)
    DATA(MSB,LSB): Message body (28 bytes), 14 pairs of bytes (MSB,LSB)
       1(  5,  6): PM 1.0 [ug/m3] (TSI standard)
       2(  7,  8): PM 2.5 [ug/m3] (TSI standard)
       3(  9, 10): PM 10. [ug/m3] (TSI standard)
       4( 11, 12): PM 1.0 [ug/m3] (std. atmosphere)
       5( 13, 14): PM 2.5 [ug/m3] (std. atmosphere)
       6( 15, 16): PM 10. [ug/m3] (std. atmosphere)
       7( 17, 18): num. particles with diameter > 0.3 um in 100 cm3 of air
       8( 19, 19): num. particles with diameter > 0.5 um in 100 cm3 of air
       9( 21, 22): num. particles with diameter > 1.0 um in 100 cm3 of air
      10( 23, 24): num. particles with diameter > 2.5 um in 100 cm3 of air
      11( 25, 26): num. particles with diameter > 5.0 um in 100 cm3 of air
      12( 27, 28): num. particles with diameter > 10. um in 100 cm3 of air
      13( 29, 30): Reserved
      14( 31, 32): cksum=byte01+..+byte30
    """

    measurements = {}

    offset = 1  # Message data starts at the 2nd pair
    for i, value in enumerate(PLANTOWER1[SUPPORTED_VALUES]):
        byte = (offset + i) * 2
        measurements[value] = sum_bytes(data[byte], data[byte + 1])
    byte = 13
    measurements['version'] = data[byte * 2]
    measurements['error'] = data[(byte * 2) + 1]
    byte = 14
    measurements['checkcode_h'] = data[byte * 2]
    measurements['checkcode_l'] = data[(byte * 2) + 1]
    return measurements

PLANTOWER1 = {
    "name": "Plantower PMS1003/5003,7003",
    STARTBLOCK: bytearray([0x42, 0x4d]),
    RECORD_LENGTH: 32,
    RECORD_CB: parse_plantower,
    BAUD_RATE: 9600,
    SUPPORTED_VALUES: [PM_1_0, PM_2_5, PM_10,
                       PM_ATM_1_0, PM_ATM_2_5, PM_ATM_10,
                       DB_0_3, DB_0_5, DB_1_0,
                       DB_2_5, DB_5_0, DB_10_0]
}
