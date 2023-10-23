# PyURLUnshortner
A simple Python URL unshortner

Quick and dirty script i wrote to track down phishing URLs. Few lines of code to unshorten URLs tracking HTTP connections through redirects, with timeout.

$ python3 unshortner.py -u http://zerozone.it
Hop     Time            Code    URL
1       618.384587 ms   301     https://zerozone.it/
2       1027.798862 ms  301     https://www.zerozone.it/
3       1148.642249 ms  200     https://www.zerozone.it/