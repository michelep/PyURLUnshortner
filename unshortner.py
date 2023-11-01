#!/usr/bin/env python3
#
# Simple Python3 URL unshortner
#
# by Michele <o-zone@zerozone.it> Pinassi
#
# v0.0.4 - Added proxy and cookie support
# v0.0.3 - Small refactor using classes
# v0.0.2 - Some minor fixes
# v0.0.1 - First release

import requests
import getopt, sys
import validators
import time

class Unshortner:
    def __init__(self, target, proxy=None, cookie=None):
        self.target = target
        self.hop = 1
        self.proxy = proxy
        self.cookie = cookie

    def _get_session(self):
        session = requests.session()
        if self.proxy is not None:
            proxy_servers = {
                'http': self.proxy,
                'https': self.proxy,
            }
            session.proxy = proxy_servers
            print("--> proxy %s"%self.proxy)
        return session

    def start(self):
        self._do_request(self.target)

    def _do_request(self, url):
        timer = time.perf_counter()
        session = self._get_session()
        try:
            r = session.get(url, allow_redirects=False, cookies=self.cookie)
        except Exception as e:
            print(str(e))
            return False
        self.cookies = requests.cookies.RequestsCookieJar()
        try:
            if 'location' in r.headers:
                print("%d\t%fms\t%d\t%s"%(self.hop,(time.perf_counter()-timer)*1000,r.status_code,r.headers['location']))
                self.hop = self.hop + 1
                return self._do_request(r.headers['location'])
        except:
            None

        print("%d\t%fms\t%d\t%s"%(self.hop,(time.perf_counter()-timer)*1000,r.status_code,r.url))
        return False

def usage():
    print("""Just a simple command-line URL unshortner 

Usage:

-h for this help
-u [target url]

Optional:

-p [proxy] 
-c [cookie]

Example:

%s -u http://www.zerozone.it
    """%sys.argv[0])

def main():
    target = proxy = cookie = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:p:c:", ["help","url=","proxy=","cookie="])
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
        elif o in ("-p", "--proxy"):
            proxy = a
        elif o in ("-c", "--cookie"):
            cookie = a
    
    if target is None:
        usage()
        sys.exit(1)
    elif not validators.url(target):
        print("Invalid URL %s"%target)
        usage()
        sys.exit(2)

    print("Hop\tTime\t\tCode\tURL")

    unshortener = Unshortner(target,proxy,cookie)
    unshortener.start()

if __name__ == "__main__":
    main()
