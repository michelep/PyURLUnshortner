#!/usr/bin/env python3
#
# Simple Python3 url unshortner
#
# by Michele <o-zone@zerozone.it> Pinassi
#

import requests
import getopt, sys
import validators
import time

history = list()

def usage():
    print("Usage:\n-h for help\n-u [target url]")

def do_request(url, hop=1):
    timer = time.perf_counter()
    r = requests.get(url, allow_redirects=False)
    try:
        if r.headers['location']:
            print("%d [%f ms]: %s [%d]"%(hop,(time.perf_counter()-timer)*1000,r.headers['location'],r.status_code))
            do_request(r.headers['location'], hop+1)
    except:
        return r.status_code

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:", ["help","url="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-u", "--url"):
            target = a
    if not validators.url(target):
        print("Invalid URL %s"%target)
        usage()
        sys.exit(2)

    do_request(target)

if __name__ == "__main__":
    main()
