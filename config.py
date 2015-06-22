import logging

# log level
loglevel = logging.INFO
# directory for log files
logdir = '/tmp'
# name for root logger
rootlogger = 'root'

# base URL for changesets
changeset_base_url = 'http://planet.osm.org/replication/changesets/'

# debug mode
debug = True

# check interval for new changesets, in seconds
check_interval = 5

# latest retrieved sequence number
sequence = 0