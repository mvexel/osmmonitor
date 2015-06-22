#!/usr/bin/env python

import requests
import config
import yaml
import os

def latest_sequence_id():
    state_url = os.path.join(config.changeset_base_url, 'state.yaml')
    response = requests.get(state_url)
    state = yaml.load(response.text)
    return state['sequence']