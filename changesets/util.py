#!/usr/bin/env python

import requests
import config
import yaml
import os
import logging
import zlib
import log

logger = log.get_logger()

def latest_sequence_id():
    state_url = os.path.join(config.changesets_base_url, 'state.yaml')
    logger.debug('getting state from {}'.format(state_url))
    response = requests.get(state_url)
    if not response.ok:
        logger.warning('could not get statefile from OSM')
        return None
    state = yaml.load(response.text)
    if not state or not 'sequence' in state:
        logger.warning('could not parse statefile from OSM')
        return None
    return state['sequence']

def url_from_sequence(sequence):
    sequence = str(sequence).zfill(9)
    sequence_path = '/'.join([sequence[i:i+3] for i in range(0, len(sequence), 3)])
    return os.path.join(config.changesets_base_url, '{}.osm.gz'.format(sequence_path))

def parse_gz_response(response):
    out = ''
    chunk_size = 1000
    d = zlib.decompressobj(16+zlib.MAX_WBITS)
    for chunk in response.iter_content(chunk_size):
        out += d.decompress(chunk)
    out += d.flush()
    return out