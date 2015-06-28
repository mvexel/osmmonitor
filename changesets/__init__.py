#!/usr/bin/env python

import config
import util
import log
import xmltodict
import requests
import os

class OSMChangesetsMeta():
    """A batch of OSM Changeset metadata"""

    SEQUENCE = 0

    content = {}
    XML = None

    def latest_from_osm(self):
        """returns the latest OSM changesets metadata."""

        import yaml
        import zlib
        import untangle

        logger = log.get_logger()

        try:
            new_changesets_meta = self.from_osm() 
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

    def from_osm(sequence=None):
        """retrieve changesets metadata from OSM.
        If sequence ID is passed in, retrieve that particular
        changesets metadata file. Otherwise gets the latest
        changesets metadata."""

        if sequence is None:
            sequence = util.latest_sequence_id()
            logger.debug('sequence is {}'.format(sequence))
        if sequence > config.sequence:
            url = util.url_from_sequence(sequence)
            logger.debug('url is {}'.format(url))
            response = requests.get(url, stream=True)
            if not response.ok:
                logger.error('could not get changesets meta sequence {}'.format(sequence))
            config.sequence = sequence
            logger.debug('config.sequence is now {}'.format(config.sequence))
            return util.parse_gz_response(response)
        else:
            logger.info('nothing new.')
        return None

    @classmethod
    def latest_from_sequence(cls, sequence_id):
        pass
