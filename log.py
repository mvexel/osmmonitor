#!/usr/bin/env python

import logging
import config
import os


def setup_logger(name=None):
    """Set up the logger."""

    if name is None:
        name = config.rootlogger
    logger = logging.getLogger(name)

    filehandler = logging.FileHandler(os.path.join(config.logdir, '{}.log'.format(__name__)))
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    filehandler.setFormatter(formatter)

    if config.debug:
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        logger.addHandler(streamhandler)
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(config.loglevel)


def get_logger(name=None):
    """Get the named (or root) logger"""

    if name is None:
        name = config.rootlogger
    return logging.getLogger(name) or None