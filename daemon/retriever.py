#!/usr/bin/env python

from daemon import Daemon
from changeset import retrieve, stash
import sched
import time


class ChangesetRetrieverDaemon(Daemon):
    """Daemon to retrieve OSM Changesets in the background"""

    def run(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        xml = retrieve.from_osm(scheduler)
        stash.elasticsearch(xml)
        scheduler.run()
