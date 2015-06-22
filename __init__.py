#!/usr/bin/env python

from daemon import retriever
import config

changesetretriever = retriever.ChangesetRetrieverDaemon(
    '/tmp/changeset_retriever.pid')
if config['debug']:
    changesetretriever.run()
else:
    changesetretriever.start()
