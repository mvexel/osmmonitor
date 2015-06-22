#!/usr/bin/env python

import logging

logger = logging.getLogger('root')

def elasticsearch(xml):
    logger.info('stashing changeset in es')
    logger.info(xml)