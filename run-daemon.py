#!/usr/bin/env python

import os
import config
import log
from daemon.retriever import ChangesetRetrieverDaemon
from changeset import OSMChangeset

if __name__ == '__main__':

    # set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='/tmp/osmmonitor.log',
                        filemode='w')

    logger = logging.getLogger(__name__)
    if config.debug:
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    logger.info('logger initiated')

    # start retriever daemon
    changeset_retriever = ChangesetRetrieverDaemon(
        os.path.join(config.tempdir, 'changeset_retriever.pid'))
    if config.debug:
        changeset_retriever.run()
    else:
        changeset_retriever.start()
