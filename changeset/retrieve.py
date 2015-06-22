#!/usr/bin/env python

from changeset import util, stash
import logging
import requests
import config

logger = logging.getLogger('root')


def from_osm(scheduler=None, sequence=None):
    if sequence is None:
        sequence = util.latest_sequence_id()
    if sequence > config.sequence:
        url = util.sequence_as_path(sequence)
        response = requests.get(url, stream=True)
        if not response.ok:
            logger.error('could not get changeset {}'.format(sequence))
        if scheduler:
            scheduler.enter(config.check_interval, 1, from_osm, (scheduler,))
        config.sequence = sequence
        return util.parse_gz_response(response)
    return None