#!/usr/bin/env python

import logging

logger = logging.getLogger('root')

def elasticsearch(changeset_xml):
    logger.info('stashing changeset in es')
    logger.info(changeset_xml)