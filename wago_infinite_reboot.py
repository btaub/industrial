
#!/usr/bin/env python

#---------------------------------------------------------------------------#
# send restart cmd to wago 750-352
#
# requires pymodbus
#---------------------------------------------------------------------------#

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import logging
import time
logging.basicConfig()
log = logging.getLogger()
#log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--rhost" ,help="aatest")
parser.add_argument("--rport", type=int)
args = parser.parse_args()
parser.set_defaults(rport=502)

client = ModbusClient(args.rhost, port=args.rport)
client.connect()

#log.info("Restarting WAGO 750-352")

# write value of 0xAA55 to register address 0x8256 on UID 1
# from pg 185 of the manual for the 750-x series of devices
while True:
    log.info("Restarting WAGO 750-352")
    rq = client.write_register(8256, 0xaa55, unit=1)
    log.info("Sent, sleeping for 6 seconds")
    time.sleep(6)

client.close()
