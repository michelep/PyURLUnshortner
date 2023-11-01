#!/usr/bin/env python3
#
# Simple Python3 url unshortner
#
# by Michele <o-zone@zerozone.it> Pinassi
#
# v0.0.3 - Small refactor using classes
# v0.0.2 - Some minor fixes
# v0.0.1 - First release

import requests
import getopt, sys
import validators
import time

class Unshortner:
    def __init__(self, target, proxies=None, cookies=None):
        self.target = target
        self.hop = 1
        self.proxies = proxies
        self.cookies = cookies

    def _get_session(self):
        session = requests.session()
        if self.proxies is not None:
            session.proxies = self.proxies
        return session

    def start(self):
        self._do_request(self.target)

    def _do_request(self, url):
        timer = time.perf_counter()
        session = self._get_session()
        try:
            r = session.get(url, allow_redirects=False, cookies=self.cookies)
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
    print("Usage:\n-h for help\n-u [target url] -p [proxy] -c [cookie]")

def main():
    target = proxies = cookies = None
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
        elif o in ("-p", "--proxy"):
            proxies.append(a)
        elif o in ("-c", "--cookie"):
            cookies.append(a)
    
    if not validators.url(target):
        print("Invalid URL %s"%target)
        usage()
        sys.exit(2)

    print("Hop\tTime\t\tCode\tURL")

    unshortener = Unshortner(target)
    unshortener.start()

if __name__ == "__main__":
    main()
