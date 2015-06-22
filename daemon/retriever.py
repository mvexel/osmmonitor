#!/usr/bin/env python

from daemon import Daemon
from changeset import retrieve
import sched
import time


class ChangesetRetrieverDaemon(Daemon):
    """Daemon to retrieve OSM Changesets in the background"""

    def run(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        retrieve.from_osm(scheduler)
        scheduler.run()
