#!/usr/bin/env python3
'''
 send restart cmd to wago 750-xxx

 requires pymodbus
'''
import time
import socket
import argparse
from pymodbus.client import ModbusTcpClient as ModbusClient

parser = argparse.ArgumentParser()
parser.add_argument("--rhost" ,help="PLC ip address")
parser.add_argument("--rport", type=int, default=502)
args = parser.parse_args()

# Check socket
def check_device_status():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((args.rhost, args.rport))
        print(f"Socket connected: {s}")

        return True

    except Exception as e:
        print(f"{args.rhost} is down, exception message: {e}")

        return False

# write value 0xAA55 to register address 0x8256 on UID 1
# from pg 185 of the manual for the 750-xxx series of devices
while True:
    try:
        is_up = check_device_status()
        if is_up:
            client = ModbusClient(args.rhost, port=args.rport)
            client.connect()

            print("\nRestarting WAGO 750-352\n")
            req = client.write_register(8256, 0xAA55, device_id=1, no_response_expected=True)

            client.close()
            time.sleep(.5)
    except Exception as e:
        print(f"Exception in main: {e}...")

