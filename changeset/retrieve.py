#!/usr/bin/env python

from changeset import util

def from_osm(scheduler=None, sequence=None):
    print 'retrieving from osm'
    if sequence is None:
        sequence = util.latest_sequence_id()
    print sequence