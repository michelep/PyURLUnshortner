#!/usr/bin/env python3
#
# Simple Python3 url unshortner
#
# by Michele <o-zone@zerozone.it> Pinassi
#
# v0.0.2 - Some minor fixes
# v0.0.1 - First release


import requests
import getopt, sys
import validators
import time

history = list()

hop = 1 # Hop counter

def usage():
    print("Usage:\n-h for help\n-u [target url]")

def do_request(url, cookies=False):
    global hop 
    timer = time.perf_counter()
    r = requests.get(url, allow_redirects=False, cookies=cookies)
    cookies = requests.cookies.RequestsCookieJar()
    try:
        if 'location' in r.headers:
            print("%d\t%f ms\t%d\t%s"%(hop,(time.perf_counter()-timer)*1000,r.status_code,r.headers['location']))
            hop = hop + 1
            return do_request(r.headers['location'], cookies)
    except:
        None

    print("%d\t%f ms\t%d\t%s"%(hop,(time.perf_counter()-timer)*1000,r.status_code,r.url))
    return False

def main():
    target = ""
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

    print("Hop\tTime\t\tCode\tURL")
    do_request(target)

if __name__ == "__main__":
    main()
