#!/usr/bin/env python

import config
import util
import retrieve
import log

class OSMChangeset():
    """An OSM Changeset"""

    SEQUENCE = 0

    content = {}

    def latest_from_osm(self):
        """returns the latest OSM changeset."""

        import yaml
        import requests
        import os
        import zlib
        import untangle

        # get logger
        logger = log.get_logger(config.rootlogger)
        logger.info('retrieving changeset')

        try:
            content = retrieve.from_osm()
        except Exception:
            logger.error('could not retrieve changeset from OSM')

    def __init__(self):
        """initialize a changeset object"""


    @classmethod
    def latest_from_sequence(cls, sequence_id):
        pass
