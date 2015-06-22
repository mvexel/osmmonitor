#!/usr/bin/env python

from changeset import util, stash
import logging
import requests

logger = logging.getLogger('root')


def from_osm(scheduler=None, sequence=None):
    if sequence is None:
        sequence = util.latest_sequence_id()
    url = util.sequence_as_path(sequence)
    response = requests.get(url, stream=True)
    if not response.ok:
        logger.error('could not get changeset {}'.format(sequence))
    stash.elasticsearch(util.parse_gz_response(response))