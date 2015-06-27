#!/usr/bin/env python

from daemon import Daemon
from changeset import OSMChangeset
import sched
import time
import config
import log

logger = log.get_logger(config.rootlogger)


class ChangesetRetrieverDaemon(Daemon):

    """Daemon to retrieve OSM Changesets in the background"""

    def run(self):
        logger.info('running retriever daemon')
        scheduler = sched.scheduler(time.time, time.sleep)
        changeset = OSMChangeset()
        changeset.latest_from_osm()
        scheduler.run()
