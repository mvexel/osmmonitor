#!/usr/bin/env python

import config
import util
import log
import xmltodict
import requests
import os

class OSMAugmentedDiff():
    """An Augmented Diff"""

    SEQUENCE = 0

    content = {}
    XML = None

    def latest_from_overpass(self):
        """returns the latest augmented diff."""

        logger = log.get_logger()
        try:
            new_diff = self.from_overpass()
            if new_diff is not None:
                self.XML = new_diff
                return True
        except Exception as e:
            logger.error('could not retrieve augmented diff')
            logger.debug(e.message)
            return False

    def __init__(self):
        """initialize an augmented diff object"""

    def as_dict(self):
        """returns the augmented diff as a python dictionary"""

        logger = log.get_logger()
        diff_dict = xmltodict.parse(self.xml)
        if 'osm' in diff_dict:
            return diff_dict['osm']
        else:
            logger.error('no osm root element in diff file')
            return None

    def from_overpass(self, sequence=None):
        """retrieve augmented diff from Overpass API.
        If sequence ID is passed in, retrieve that particular
        augmented diff file. Otherwise gets the latest
        augmented diff."""

        logger = log.get_logger()

        if sequence is None:
            sequence = util.latest_diff_sequence()
        logger.debug('sequence is {}'.format(sequence))
        if sequence > config.diffs_sequence:
            url = os.path.join(
                config.overpass_augmented_diffs_url,
                '?id={}'.format(sequence))
            logger.debug('url is {}'.format(url))
            response = requests.get(url)
            if not response.ok:
                logger.error('could not get augmented diff sequence {}'.format(sequence))
            config.diffs_sequence = sequence
            return response.text
        else:
            logger.info('nothing new.')
        return None

    @classmethod
    def latest_from_sequence(cls, sequence_id):
        pass
