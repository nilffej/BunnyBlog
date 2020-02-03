#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/p00/")
sys.path.insert(0,"/var/www/p00/p00/")

import logging
logging.basicConfig(stream=sys.stderr)

from p00 import app as application
