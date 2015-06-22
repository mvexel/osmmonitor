#!/usr/bin/env python

import requests
import config
import yaml
import os
import logging
import zlib

logger = logging.getLogger(config.rootlogger)


def latest_sequence_id():
    state_url = os.path.join(config.changeset_base_url, 'state.yaml')
    logger.info('getting state from {}'.format(state_url))
    response = requests.get(state_url)
    state = yaml.load(response.text)
    return state['sequence']

def sequence_as_path(sequence):
    sequence = str(sequence).zfill(9)
    sequence_path = '/'.join([sequence[i:i+3] for i in range(0, len(sequence), 3)])
    return os.path.join(config.changeset_base_url, '{}.osm.gz'.format(sequence_path))

def parse_gz_response(response):
    out = ''
    chunk_size = 1000
    d = zlib.decompressobj(16+zlib.MAX_WBITS)
    for chunk in response.iter_content(chunk_size):
        out += d.decompress(chunk)
    out += d.flush()
    return out