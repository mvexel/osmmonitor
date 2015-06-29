#!/usr/bin/env python

"""OSM Monitor Daemon Runner

Usage:
  run_daemon.py (start|stop) (changesets|diffs) [--debug]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --debug       Debug mode
"""

__version__ = "OSM Monitor 0.1"

import os
import config
import log
import sched
import time
from elasticsearch import Elasticsearch
from daemon import Daemon
from changesets import OSMChangesetsMeta
from diffs import OSMAugmentedDiff
from docopt import docopt


class ChangesetsMetaRetrieverDaemon(Daemon):
    """daemon class to handle changesets meta retrieval"""

    scheduler = sched.scheduler(time.time, time.sleep)
    changesets = OSMChangesetsMeta()
    logger = log.get_logger()

    def run(self):
        logger.info('starting changesets meta retriever daemon...')
        self.retrieve_changesets(self.scheduler)
        self.scheduler.run()

    def retrieve_changesets(self, scheduler):
        logger.debug('getting changesets')
        if self.changesets.latest_from_osm():
            self.stash_changesets()
        scheduler.enter(config.check_interval, 1, self.retrieve_changesets, (self.scheduler,))

    def stash_changesets(self):
        """stash retrieved changesets in ES"""
        try:
            es = Elasticsearch()
            logger.debug('sequence is {}'.format(config.changesets_sequence))
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


class DiffsRetrieverDaemon(Daemon):
    """daemon class to handle diff retrieval"""

    scheduler = sched.scheduler(time.time, time.sleep)
    diffs = OSMAugmentedDiff()
    logger = log.get_logger()

    def run(self):
        logger.info('starting diffs retriever daemon...')
        self.retrieve_diffs(self.scheduler)
        self.scheduler.run()

    def retrieve_diffs(self, scheduler):
        logger.debug('getting diffs')
        if self.diffs.latest_from_overpass():
            self.stash_diffs()
        scheduler.enter(config.check_interval, 1, self.retrieve_diffs, (self.scheduler,))

    def stash_diffs(self):
        """stash retrieved diffs in ES"""
        try:
            es = Elasticsearch()
            logger.debug('sequence is {}'.format(config.diffs_sequence))
            diffs = self.diffs.as_dict()
            for diff in diffs:
                logger.debug('storing diff for {}'.format(config.diffs_sequence))
                es.index(
                    index="osm",
                    doc_type="diffs",
                    id=config.diffs_sequence,
                    body=diff)
        except Exception as e:
            logger.error('could not store diffs in ES')
            logger.debug(e.message)


if __name__ == '__main__':

    #arg parsing
    arguments = docopt(__doc__, version=__version__)

    #set up logging
    log.setup_logger(debug=arguments['--debug'])
    logger = log.get_logger()

    # instantiate a changesets retriever
    changesets_retriever = ChangesetsMetaRetrieverDaemon(
        os.path.join(
            config.tempdir,
            '{}.pid'.format('changesets_{}'.format(__name__))))

    # and a changesets retriever
    diffs_retriever = DiffsRetrieverDaemon(
        os.path.join(
            config.tempdir,
            '{}.pid'.format('diffs_{}'.format(__name__))))

    # handle debugging mode
    if arguments['--debug']:
        logger.debug('debugging mode')
        changesets_retriever.verbose = 1
        diffs_retriever.verbose = 1
    else:
        changesets_retriever.verbose = 0
        diffs_retriever.verbose = 0

    # stop daemons
    if arguments['stop']:
        # stop the daemon(s)
        if arguments['changesets']:
            changesets_retriever.stop()
            print('changesets retriever stopped.')
        if arguments['diffs']:
            diffs_retriever.stop()
            print('diffs retriever stopped.')

    # start daemons
    if arguments['start']:
        # start changesets retriever daemon
        if arguments['changesets']:
            if arguments['--debug']:
                # run in foreground
                changesets_retriever.run()
            else:
                # run in background, output something meaningful
                print('starting changesets retriever...')
                changesets_retriever.start()
                print('started!')

        # start diffs retriever daemon
        if arguments['diffs']:
            if arguments['--debug']:
                # run in foreground
                diffs_retriever.run()
            else:
                # run in background, output something meaningful
                print('starting diffs retriever...')
                diffs_retriever.start()
                print('started!')
