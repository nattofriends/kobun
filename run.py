#!/usr/bin/env python2

import logging
logging.basicConfig(level=logging.INFO)

import kobun
import json

with open("config.json", "r") as f:
    config = json.load(f)

kobun.run(config)

