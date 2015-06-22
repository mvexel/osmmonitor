#!/usr/bin/env python

from changeset import util
import logging

logger = logging.getLogger('root')

def from_osm(scheduler=None, sequence=None):
    if sequence is None:
        sequence = util.latest_sequence_id()
    logger.info('getting sequence {}'.format(sequence))