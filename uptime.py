import subprocess
import logging
import time
import urllib2

URL = "http://eero.com/"
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

while True:
    try:
        tries += 1
        urllib2.urlopen(URL, timeout=5).read()
        if not online:
            online = True
            came_online = time.localtime()
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
        print "not ok"
        logit()
        if online:
            online = False
            went_offline = time.localtime()
    time.sleep(1)
