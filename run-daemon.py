#!/usr/bin/env python

import os
import config
import log
from daemon import Daemon

class ChangesetRetrieverDaemon(Daemon):
    """daemon class to handle changeset retrieval"""

    def run(self):
        logger = log.get_logger()
        logger.info('starting daemon...')

if __name__ == '__main__':

    #set up logging
    log.setup_logger()
    
    # start retriever daemon
    retriever = ChangesetRetrieverDaemon(
        os.path.join(
            config.tempdir,
            '{}.pid'.format(__name__)))
    if config.debug:
        retriever.verbose = 1
        retriever.start()
    else:
        retriever.verbose = 0
        retriever.run()