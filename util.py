#!/usr/bin/env python

import requests
import config
import yaml
import os
import zlib
import log
import re

logger = log.get_logger()

def latest_changeset_sequence():
    state_url = os.path.join(config.osm_changesets_base_url, 'state.yaml')
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

def latest_diff_sequence():
    state_url = os.path.join(config.osm_minutelies_base_url, 'state.txt')
    logger.debug('getting state from {}'.format(state_url))
    response = requests.get(state_url)
    if not response.ok:
        logger.warning('could not get statefile from OSM')
        return None
    match = re.search(r'sequenceNumber=(\d+)', response.text)
    if not match:
        logger.error('state file is borked, does not contain sequenceNumber')
        return None
    logger.debug(match)
    seq = match.group(1)
    logger.debug(seq)
    return seq


def url_from_sequence(sequence):
    sequence = str(sequence).zfill(9)
    sequence_path = '/'.join([sequence[i:i+3] for i in range(0, len(sequence), 3)])
    return os.path.join(config.osm_changesets_base_url, '{}.osm.gz'.format(sequence_path))

def parse_gz_response(response):
    out = ''
    chunk_size = 1000
    d = zlib.decompressobj(16+zlib.MAX_WBITS)
    for chunk in response.iter_content(chunk_size):
        out += d.decompress(chunk)
    out += d.flush()
    return out