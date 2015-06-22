#!/usr/bin/env python

from python-daemon import Daemon


class ChangesetRetrieverDaemon(Daemon):
    """Daemon to retrieve OSM Changesets in the background"""

    def run(self):
