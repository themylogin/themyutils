import json
import logging
import time
import urllib2

logger = logging.getLogger(__name__)

class RestfulApiPoller(object):
    def __init__(self, url, reconnect_timeout=5):
        self.url = url
        self.reconnect_timeout = reconnect_timeout

    def __iter__(self):
        version = None
        while True:
            headers = {}
            if version is not None:
                headers = {"Range": "%d-" % version}

            try:
                data = json.loads(urllib2.urlopen(urllib2.Request(self.url, None, headers)).read())
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                logger.exception("Error loading %s" % self.url)
                time.sleep(self.reconnect_timeout)
                continue

            version = data["version"]
            logger.info("Loaded %s version %d", self.url, version)

            yield data
