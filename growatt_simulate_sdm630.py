#!/usr/bin/env python

# Simulate SDM630 for testing export limitation on Growatt MIC 600TL-X

import sys
import serial
import binascii
import struct
import time

def calc_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos 
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc


def main():

    # process arguments
    if len(sys.argv) != 3:
        print("USAGE: growatt_simulate_sdm630.py SERIALPORT TOTAL_SYSTEM_POWER_IN_WATT")
        exit()
    port = sys.argv[1]
    total_system_power = int(sys.argv[2])    

    # open serial port of RS485 interface
    s = serial.Serial(port=port, baudrate=9600)

    # initialize receive buffer
    recbuffer = [0] * 8

    try:
        while True:

            # read in one byte and add it to the receive buffer, trim buffer to 8 bytes
            data = s.read(1)
            recbuffer = recbuffer + list(data)
            recbuffer = recbuffer[-8:]

            # process only if crc matches
            if calc_crc(recbuffer) != 0:
                continue

            # show packet
            print(time.time(), binascii.hexlify(bytes(recbuffer)))

            # extract parameters from packet
            slaveadr = recbuffer[0]
            functioncode = recbuffer[1]
            address = recbuffer[2] << 8 | recbuffer[3]
            wordsize = recbuffer[4] << 8 | recbuffer[5]                     

            # process read request for register 30053 (Total system power in Watt) 
            if slaveadr == 2 and address == 52:
                
                # show packet parameters
                print(" process register read ", slaveadr, functioncode, address, wordsize)

                # construct response
                wordsize = 2
                response = [0x02, functioncode, wordsize * 2]
                response.extend(struct.pack('>f', total_system_power))
                crc = calc_crc(response)
                response.append(int(crc & 0xff))
                response.append(int((crc >> 8) & 0xff))

                # show response and send it out
                print(" response", response)
                s.write(response)

            # finished processing of packet, clear buffer
            recbuffer = [0] * 8

    finally:
        s.close()

if __name__ == "__main__":
    main()
