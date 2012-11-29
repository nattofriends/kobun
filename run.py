#!/usr/bin/env python2

import logging
logging.basicConfig(level=logging.INFO)

import kobun
import json

import sys

kobun.run("config.json" if len(sys.argv) < 2 else sys.argv[1])

