#!/usr/bin/env python

from daemon import Daemon
import requests
import yaml

REPLICATION_BASE = 'http://planet.osm.org/replication/changesets/'
# create daemon to get changesets

class ChangesetRetrieverDaemon(Daemon):

    import sched, time

    def periodic(scheduler, interval, action, actionargs=()):
        scheduler.enter(interval, 1, periodic,
            (scheduler, interval, action, actionargs))
        action(*actionargs)

    def get_latest_changeset():
        print 'getting latest changeset'

    def run(self):
        print 'daemon runs'
        import sched, time
        scheduler = sched.scheduler(time.time, time.sleep)






if __name__ == '__main__':
    changeset_retriever = ChangesetRetrieverDaemon('/tmp/changeset_retriever.pid')
    changeset_retriever.start()
    changeset_retriever.stop()