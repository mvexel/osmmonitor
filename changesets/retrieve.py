#!/usr/bin/env python

import os
from changesets import util, stash
import logging
import requests
import config
import log

logger = log.get_logger()


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