#!/usr/bin/env python3

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from datetime import datetime
import time

client = ModbusClient("challenges.icsjwgctf.com",5020)
client.connect()

while True:
    rr = client.read_discrete_inputs(0, 16, unit=0)
    print("\n[+]",datetime.now(),"\n")
    for dI in range(0,16):
        print("%s: %s" %(dI , rr.bits[dI]))

    time.sleep(2)
    client.close()

''' Output:
[+] 2022-04-24 13:36:18.211965

0: True
1: False
2: False
3: True
4: True
5: False
6: True
7: True
8: True
9: False
10: True
11: True
12: False
13: True
14: True
15: True
'''
