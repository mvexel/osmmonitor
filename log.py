#!/usr/bin/env python

import logging
import config
import os


def setup_logger(name=None):
    if name is None:
        name = config.rootlogger
    logger = logging.getLogger(name)
    logger.setLevel(config.loglevel)
    filehandler = logging.FileHandler(os.path.join(config.logdir, '{}.log'.format(__name__)))
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    filehandler.setFormatter(formatter)
    if config.debug:
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        logger.addHandler(streamhandler)
    return logger

def get_logger(name=None):
    if name is None:
        name = config.rootlogger
    return logging.getLogger(name) or None