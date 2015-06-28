#!/usr/bin/env python

import os
import config
import log
import sched
import time
from elasticsearch import Elasticsearch
from daemon import Daemon
from changesets import OSMChangesetsMeta


class ChangesetsMetaRetrieverDaemon(Daemon):
    """daemon class to handle changesets meta retrieval"""

    scheduler = sched.scheduler(time.time, time.sleep)
    changesets = OSMChangesetsMeta()
    logger = log.get_logger()

    def run(self):
        logger.info('starting daemon...')
        self.retrieve_changesets(self.scheduler)
        self.scheduler.run()

    def retrieve_changesets(self, scheduler):
        logger.debug('getting changesets')
        if self.changesets.latest_from_osm():
            logger.debug('got a new one!')
            self.stash_changesets()

        scheduler.enter(config.check_interval, 1, self.retrieve_changesets, (self.scheduler,))

    def stash_changesets(self):
        """stash retrieved changesets in ES"""
        try:
            #logger = log.get_logger()
            es = Elasticsearch()
            logger.debug('sequence is {}'.format(config.sequence))
            changesets_meta = self.changesets.as_dict()
            for changeset_meta in changesets_meta:
                logger.debug('storing changeset meta for {}'.format(changeset_meta['@id']))
                es.index(
                    index="osm",
                    doc_type="changesets",
                    id=changeset_meta['@id'],
                    body=changeset_meta)
        except Exception as e:
            logger.error('could not store changesets in ES')
            logger.debug(e.message)

if __name__ == '__main__':

    #set up logging
    log.setup_logger()
    logger = log.get_logger()

    # start retriever daemon
    retriever = ChangesetsMetaRetrieverDaemon(
        os.path.join(
            config.tempdir,
            '{}.pid'.format(__name__)))
    if config.debug:
        logger.debug('debugging mode')
        retriever.verbose = 1
        retriever.run()
    else:
        retriever.verbose = 0
        retriever.start()