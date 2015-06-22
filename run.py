#!/usr/bin/env python

from daemon import retriever
import logging
import config
import os
import log

logger = log.setup_logger(config.rootlogger)

changesetretriever = retriever.ChangesetRetrieverDaemon(
    '/tmp/changeset_retriever.pid')
if config.debug:
    changesetretriever.run()
else:
    changesetretriever.start()
