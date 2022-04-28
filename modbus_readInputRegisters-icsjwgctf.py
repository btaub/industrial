#!/usr/bin/env python3

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from datetime import datetime
import time

client = ModbusClient("challenges.icsjwgctf.com",5020)
client.connect()

while True:
    rr = client.read_input_registers(0, 24, unit=0)
    print("\n[+]",datetime.now(),"\n")
    for iR in range(0,24):
        print("%s: %s" %(iR , rr.registers[iR]))

    time.sleep(1)
    client.close()

'''Output:
[+] 2022-04-24 15:43:34.834891

0: 52
1: 639
2: 910
3: 88
4: 8238
5: 6064
6: 73
7: 758
8: 161
9: 731
10: 63
11: 97
12: 9239
13: 8966
14: 49
15: 294
16: 5950
17: 226
18: 39
19: 1
20: 9
21: 9
22: 90
23: 8
'''
