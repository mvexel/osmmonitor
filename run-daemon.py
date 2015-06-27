#!/usr/bin/env python

import os
import config
import log
import sched
import time
from daemon import Daemon
from changeset import OSMChangeset

class ChangesetRetrieverDaemon(Daemon):
    """daemon class to handle changeset retrieval"""

    scheduler = sched.scheduler(time.time, time.sleep)

    def run(self):
        logger = log.get_logger()
        logger.info('starting daemon...')
        self.retrieve_changeset(self.scheduler)
        self.scheduler.run()

    def retrieve_changeset(self, scheduler):
        logger.debug('getting changeset')
        changeset = OSMChangeset()
        changeset.latest_from_osm()
        scheduler.enter(config.check_interval, 1, self.retrieve_changeset, (self.scheduler,))


if __name__ == '__main__':

    #set up logging
    log.setup_logger()
    logger = log.get_logger()

    # start retriever daemon
    retriever = ChangesetRetrieverDaemon(
        os.path.join(
            config.tempdir,
            '{}.pid'.format(__name__)))
    if config.debug:
        logger.debug('debugging mode')
        retriever.verbose = 1
        retriever.start()
    else:
        retriever.verbose = 0
        retriever.run()