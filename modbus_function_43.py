#! /usr/bin/env python3

#---------------------------------------------------------------------------#
# if the PLC supports it, data from function_43 will be returned, e.g.:
#
# Schneider Electric TM221CE40TV1.1,10.100.100.100
#
# if verbose is used:
#
# +-----------------------------------------------+
# | decoded_response | encoded_response  | target |
# +-----------------------------------------------+
# Schneider Electric TM221CE40TV1.1,b'\x0e\x01\x81\x00\x00\t\x00\x12Schneider Electric\x01\nTM221CE40TV\x02\x04V1.1',10.100.100.100
#
#---------------------------------------------------------------------------#
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.mei_message import *
from pymodbus import exceptions
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--rhost" ,help="aatest")
parser.add_argument("--rport", type=int, default=502)
parser.add_argument("--uid", type=int, default=0)
parser.add_argument("-v","--verbose",action="store_true",default=False)
args = parser.parse_args()

try:
    with ModbusClient(args.rhost, port=args.rport) as client:
        client.connect()
        function_43_resp = client.execute(ReadDeviceInformationRequest(unit=args.uid))

        resp = function_43_resp.encode()
        resp = resp.replace(b'\n',b' ')
        resp = resp.replace(b'\t',b'')
        resp = resp.decode(errors='ignore')

        if args.verbose:

            print('\n+-----------------------------------------------+'
                  '\n| decoded_response | encoded_response  | target |'
                  '\n+-----------------------------------------------+'
                  f'\n{resp},{function_43_resp.encode()},{args.rhost}\n')

        else:
            print(f'{resp},{args.rhost}')

        client.close()

except exceptions.ConnectionException as e:
    print(f"\n[-] Exception: {e},{args.rhost}\n")

