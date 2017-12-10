import subprocess
import logging
import time
import urllib2

URL = "http://web.tom.org:3000/vt/"
INTERVAL = 60

logging.basicConfig(filename='./uptime.log', level=logging.INFO, \
                  format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

def logit():
    logging.info(subprocess.check_output(['/Users/tom/bin/airport', '-s']))
    logging.info(subprocess.check_output(['/Users/tom/bin/airport', '-I']))

logging.info("starting up monitoring")
logit()


while True:
    online = True
    went_offline = came_online = time.localtime()
    tries = 0
    try:
        tries += 1
        urllib2.urlopen(URL, timeout=5).read()
        if not online:
            online = True
            came_online = time.localtime()
            logging.info("came back online")
            logging.info("offline since: %s", time.asctime(went_offline))
            logit()
        if not tries % INTERVAL:
            logging.info("Checkpointing: ")
            logit()
            logging.info("Done checkpointing: ")
        logging.debug("ok: %s", time.asctime())
    except Exception as e:
        logging.info("not ok")
        print "not ok"
        logit()
        if online:
            online = False
            went_offline = time.localtime()
    time.sleep(1)
