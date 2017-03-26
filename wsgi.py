#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/forex/mt4-server/")

from api import app as application
application.secret_key = 'lofyer'
