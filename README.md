# PyURLUnshortner

A simple **Python command-line URL unshortner**

Quick and dirty script i wrote to track down phishing URLs. Few lines of code to unshorten URLs tracking HTTP connections through redirects, with timeout.

    $ python3 unshortner.py -u http://zerozone.it
    Hop Time Code URL
    1  618.384587ms 301 https://zerozone.it/
    2  1027.798862ms 301 https://www.zerozone.it/
    3  1148.642249ms 200 https://www.zerozone.it/

## Requirements

Require Python3 requests and validators, just run `pip install -r requirements.txt`