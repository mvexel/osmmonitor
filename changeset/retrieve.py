#!/usr/bin/env python

import os
from changeset import util, stash
import logging
import requests
import config


logger = logging.getLogger('root')


def from_osm(sequence=None):
    if sequence is None:
        sequence = util.latest_sequence_id()
    if sequence > config.sequence:
        url = os.path.join(
            config.changeset_base_url,
            util.sequence_as_path(sequence))
        response = requests.get(url, stream=True)
        if not response.ok:
            logger.error('could not get changeset {}'.format(sequence))
        config.sequence = sequence
        return util.parse_gz_response(response)
    return None