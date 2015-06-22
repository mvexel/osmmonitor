#!/usr/bin/env python

from python-daemon import Daemon
from ../changesets import retrieve

class ChangesetRetrieverDaemon(Daemon):
    """Daemon to retrieve OSM Changesets in the background"""

    def run(self):
        import sched
        import time
        retrieve.latest_from_osm()
        scheduler = sched.scheduler(time.time, time.sleep)