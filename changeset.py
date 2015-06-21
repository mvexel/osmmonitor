#!/usr/bin/env python


class OSMChangeset():
    """OSM Changeset handler class"""

    SEQUENCE = 0

    content = {}

    def latest_from_osm(self, scheduler, config, logger):
        """returns the latest OSM changeset.

        Arguments:
        scheduler -- application scheduler object
        config -- application config object
        logger -- application logger object"""

        import yaml
        import requests
        import os
        import zlib
        import untangle

        state = yaml.load(requests.get(os.path.join(config.osm['replication_url'], 'state.yaml')).text)

        if state['sequence'] > self.SEQUENCE:
            # get change file path
            sequence = str(state['sequence']).zfill(9)
            path = os.path.join(config.osm['replication_url'], '/'.join(sequence[i:i+3] for i in range (0, len(sequence), 3)) + '.osm.gz')

            # get the xml file and untangle it
            response = requests.get(path)
            if not response.ok:
                logger.warning('we couldn\'t fetch the changeset')
            d = zlib.decompressobj(16+zlib.MAX_WBITS)  # http://stackoverflow.com/a/2424549
            outstr = d.decompress(response.content)
            self.SEQUENCE = state['sequence']
            logger.info('getting changeset {}'.format(state['sequence']))
            self.content = untangle.parse(outstr)
        else:
            # nothing new
            logger.info('nothing new')

        # schedule the next try
        scheduler.enter(config.daemon['check_frequency'], 1, self.latest_from_osm, (scheduler, config, logger))

    def __init__(self):
        pass