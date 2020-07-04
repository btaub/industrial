
#!/usr/bin/env python

#---------------------------------------------------------------------------#
# if the PLC supports it, data from function_43 will be returned, e.g.:
#
# [+] raw_response:
# '\x0e\x01\x81\x00\x00\x06\x00\x14Schneider Electric  \x01\rBMX P34 20302\x02\x05v3.01'
#
#---------------------------------------------------------------------------#

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import logging
import sys
import argparse
from pymodbus.mei_message import *
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer

parser = argparse.ArgumentParser()
parser.add_argument("--rhost" ,help="aatest")
parser.add_argument("--rport", type=int)
args = parser.parse_args()
parser.set_defaults(rport=502)

if args.rhost == None:
    print(parser.print_help())
    sys.exit()

with ModbusClient(args.rhost, port=args.rport) as client:
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    #log.setLevel(logging.DEBUG)

client.connect()
func_43_resp = client.execute(ReadDeviceInformationRequest(unit=0))
#print("FC: %s ") % func_43_resp.function_code
#print("SUBFC: %s ") % func_43_resp.sub_function_code
print("\n[+] raw_response:\n%r\n" % func_43_resp.encode())
#print("\n[+] formatted_response: %s\n")  % (func_43_resp.encode()) # This doesn't print out correctly (something with struct fmt?)

client.close()
