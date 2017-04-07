#!/bin/bash
kill `cat /var/run/mt4-server.pid`
rm -f /var/run/mt4-server.pid
