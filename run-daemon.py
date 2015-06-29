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
from diff import OSMAugmentedDiff
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


class diffRetrieverDaemon(Daemon):
    """daemon class to handle diff retrieval"""

    scheduler = sched.scheduler(time.time, time.sleep)
    diff = OSMAugmentedDiff()
    logger = log.get_logger()

    def run(self):
        logger.info('starting diff retriever daemon...')
        self.retrieve_diff(self.scheduler)
        self.scheduler.run()

    def retrieve_diff(self, scheduler):
        logger.debug('getting diff')
        if self.diff.latest_from_overpass():
            self.stash_diff()
        scheduler.enter(config.check_interval, 1, self.retrieve_diff, (self.scheduler,))

    def stash_diff(self):
        """stash retrieved diff in ES"""
        try:
            es = Elasticsearch()
            logger.debug('sequence is {}'.format(config.diffs_sequence))
            actions = self.diff.as_dict()
            for action in actions:
                logger.debug('storing action for {}'.format(config.diffs_sequence))
                es.index(
                    index="osm",
                    doc_type="diff",
                    id=config.diffs_sequence,
                    body=action)
        except Exception as e:
            logger.error('could not store diff in ES')
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
    diff_retriever = diffRetrieverDaemon(
        os.path.join(
            config.tempdir,
            '{}.pid'.format('diff_{}'.format(__name__))))

    # handle debugging mode
    if arguments['--debug']:
        logger.debug('debugging mode')
        changesets_retriever.verbose = 1
        diff_retriever.verbose = 1
    else:
        changesets_retriever.verbose = 0
        diff_retriever.verbose = 0

    # stop daemons
    if arguments['stop']:
        # stop the daemon(s)
        if arguments['changesets']:
            changesets_retriever.stop()
            print('changesets retriever stopped.')
        if arguments['diffs']:
            diff_retriever.stop()
            print('diff retriever stopped.')

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

        # start diff retriever daemon
        if arguments['diffs']:
            if arguments['--debug']:
                # run in foreground
                diff_retriever.run()
            else:
                # run in background, output something meaningful
                print('starting diff retriever...')
                diff_retriever.start()
                print('started!')
