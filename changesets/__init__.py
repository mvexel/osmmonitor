#!/usr/bin/env python

import config
import util
import retrieve
import log
import xmltodict

class OSMChangesetsMeta():
    """A batch of OSM Changeset metadata"""

    SEQUENCE = 0

    content = {}
    XML = None

    def latest_from_osm(self):
        """returns the latest OSM changesets metadata."""

        import yaml
        import requests
        import os
        import zlib
        import untangle

        logger = log.get_logger()

        try:
            new_changesets_meta = retrieve.from_osm() 
            if new_changesets_meta is not None:
                self.XML = new_changesets_meta
                logger.debug(self.XML)
                return True
        except Exception as e:
            logger.error('could not retrieve changesets meta file from OSM')
            logger.debug(e.message)
            return False

    def __init__(self):
        """initialize a changesets metadata object"""

    def as_dict(self):
        """returns changesets metadata as a python dictionary"""

        logger = log.get_logger()
        changesets_dict = xmltodict.parse(self.XML)
        if 'changeset' in changesets_dict['osm']:
            return changesets_dict['osm']['changeset']
        else:
            logger.error('no changesets in result')
            return {}


    @classmethod
    def latest_from_sequence(cls, sequence_id):
        pass
