#!/usr/bin/env python

import os
import config
import logging
from daemon import Daemon
from changeset import OSMChangeset

# set up logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/osmmonitor.log',
                    filemode='w')

logger = logging.getLogger(__name__)
if config.application['debug']:
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

logger.info('logger initiated')


class ChangesetRetrieverDaemon(Daemon):
    """Changeset retriever daemon"""

    def run(self):
        """run the daemon"""

        import sched
        import time

        changeset = OSMChangeset()

        logger.info('daemon runs')
        scheduler = sched.scheduler(time.time, time.sleep)
        changeset.latest_from_osm(scheduler, config, logger)
        scheduler.run()

if __name__ == '__main__':

    changesetretriever = ChangesetRetrieverDaemon(
        '/tmp/changeset_retriever.pid')
    if config.application['debug']:
        changesetretriever.run()
    else:
        changesetretriever.start()
