import os
import subprocess
import logging
import time
import urllib2

URL = "http://192.168.1.4/stats.htm"
HOST = "192.168.1.254"
INTERVAL = 60
AIRPORT_BIN = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

logging.basicConfig(filename='./uptime.log', level=logging.DEBUG, \
                  format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

def logit():
    logging.debug("logit()")
    logging.info(subprocess.check_output([AIRPORT_BIN, '-s']))
    logging.info(subprocess.check_output([AIRPORT_BIN, '-I']))

online = True
went_offline = came_online = time.localtime()
tries = 0

logging.info("starting up monitoring")
logit()


def check_http(url):
    logging.debug("check_http()")
    try:
        urllib2.urlopen(url, timeout=5).read()
        return True
    except Exception as e:
        raise e


def check_ping(hostname):
    logging.debug("check_ping()")
    response = os.system("ping -c 1 -W1 " + hostname + " > /dev/null 2>&1")
    if response == 0:
        return
    else:
        raise Exception('ping failed')

while True:
    try:
        tries += 1
        check_ping(HOST)
        if not online:
            online = True
            came_online = time.localtime()
            print "ok:", time.asctime()
            logging.warning("came back online")
            logging.warning("offline since: %s", time.asctime(went_offline))
            logit()
        if not tries % INTERVAL:
            logging.info("Checkpointing: ")
            logit()
            logging.info("Done checkpointing: ")
        logging.debug("retrieval ok: %d", tries)
    except Exception as e:
        logging.error("not ok")
        print "not ok:", time.asctime()
        logit()
        if online:
            online = False
            went_offline = time.localtime()
    time.sleep(1)
