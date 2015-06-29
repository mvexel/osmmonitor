import logging
import os

# log level
loglevel = logging.WARNING
# directory for log files
logdir = '/tmp'
# temp file directory
tempdir = '/tmp'
# name for root logger
rootlogger = 'root'

# base URL for OSM replication
osm_base_url = 'http://planet.osm.org/replication/'

# base URL for changesets from OSM
osm_changesets_base_url = os.path.join(
    osm_base_url,
    'changesets')

# base URL for minutely diffs from OSM
osm_minutelies_base_url = os.path.join(
    osm_base_url,
    'minute')

# URL for augmented diffs from Overpass
overpass_augmented_diffs_url = 'http://overpass-api.de/api/augmented_diff'

# check interval for new changesets, in seconds
check_interval = 30

# latest retrieved sequence number
changesets_sequence = 0
diffs_sequence = 0